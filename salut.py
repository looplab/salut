# Copyright 2012 Loop Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__version__ = '0.1.0'
__project_url__ = 'https://github.com/looplab/salut'


from gevent import monkey
monkey.patch_select()

import gevent
import pybonjour


class Announcer(object):
    def __init__(self, name, regtype, port,
                 registered_callback=None):
        self.announced = False
        self._name = name
        self._regtype = regtype
        self._port = port
        self._registered_callback = registered_callback
        self._register_ref = None
        self._announce_task = gevent.spawn(self._announce)
        self._announce_task.link(self._announce_stop)

    def stop(self):
        self._announce_task.kill()

    def _announce(self):
        self._register_ref = pybonjour.DNSServiceRegister(
            name=self._name,
            regtype=self._regtype,
            port=self._port,
            callBack=self._register_callback)
        while True:
            ready = gevent.select.select([self._register_ref], [], [])
            if self._register_ref in ready[0]:
                pybonjour.DNSServiceProcessResult(self._register_ref)

    def _announce_stop(self, task):
        if self._register_ref:
            self._register_ref.close()
            self._register_ref = None
        self.announced = False

    def _register_callback(self, ref, flags, error, name, regtype, domain):
        # TODO: add error checking and more callbacks
        if error == pybonjour.kDNSServiceErr_NoError:
            self.announced = True
            if hasattr(self._registered_callback, '__call__'):
                self._registered_callback(domain, regtype, name)


class Browser(object):
    def __init__(self, name, regtype,
                 resolved_callback=None,
                 unresolved_callback=None):
        self.resolved = False
        self._name = name
        self._regtype = regtype
        self._timeout = 5
        self._resolved = []
        self._resolved_callback = resolved_callback
        self._unresolved_callback = unresolved_callback
        self._browse_ref = None
        self._browse_task = gevent.spawn(self._browse)
        self._browse_task.link(self._browse_stop)

    def stop(self):
        self._browse_task.kill()

    def _browse(self):
        self._browse_ref = pybonjour.DNSServiceBrowse(
            regtype=self._regtype,
            callBack=self._browse_callback)
        while True:
            ready = gevent.select.select([self._browse_ref], [], [])
            if self._browse_ref in ready[0]:
                pybonjour.DNSServiceProcessResult(self._browse_ref)

    def _browse_stop(self, task):
        if self._browse_ref:
            self._browse_ref.close()
            self._browse_ref = None
        self.resolved = False

    def _browse_callback(self, ref, flags, interfaceIndex, errorCode,
                         serviceName, regtype, replyDomain):
        if errorCode != pybonjour.kDNSServiceErr_NoError:
            # TODO: tell app that zero conf is not working
            return

        if not (flags & pybonjour.kDNSServiceFlagsAdd):
            if serviceName == self._name:
                self.resolved = False
                if hasattr(self._unresolved_callback, '__call__'):
                    self._unresolved_callback()
            return

        # TODO: check for correct service type
        if serviceName != self._name:
            return

        resolve_ref = pybonjour.DNSServiceResolve(
            0, interfaceIndex,
            serviceName, regtype, replyDomain,
            self._resolve_callback)

        try:
            while not self._resolved:
                ready = gevent.select.select(
                    [resolve_ref], [], [], self._timeout)
                if resolve_ref not in ready[0]:
                    # TODO: tell app about resolve timeout
                    break
                pybonjour.DNSServiceProcessResult(resolve_ref)
            else:
                self._resolved.pop()
        finally:
            resolve_ref.close()

    def _resolve_callback(self, ref, flags, interfaceIndex, errorCode,
                          fullname, hosttarget, port, txtRecord):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            self._resolved.append(True)
            self.resolved = True
            if hasattr(self._resolved_callback, '__call__'):
                ip = gevent.socket.gethostbyname(hosttarget)
                self._resolved_callback(ip, port)
