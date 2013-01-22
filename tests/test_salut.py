# Copyright 2012 Loop Lab
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unittest
from mock import MagicMock

import socket
import gevent
import gevent.socket

from salut import Announcer, Browser


class TestSalut(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_announce(self):
        announcer = Announcer('Test', '_salut_test._tcp', 9999)

        while not announcer.announced:
            gevent.sleep(0.05)

        announcer.stop()

    def test_announce_registered_callback(self):
        callback = MagicMock()
        announcer = Announcer(
            'Test', '_salut_test._tcp', 9999, callback.registered)

        while not announcer.announced:
            gevent.sleep(0.05)
        callback.registered.assert_called_once_with(
            'local.', '_salut_test._tcp.', 'Test')

        announcer.stop()

    def test_browse(self):
        announcer = Announcer('Test', '_salut_test._tcp', 9999)
        while not announcer.announced:
            gevent.sleep(0.05)

        browser = Browser(
            'Test', '_salut_test._tcp')

        while not browser.resolved:
            gevent.sleep(0.05)

        browser.stop()
        announcer.stop()

    def test_browse_resolved_callback(self):
        ip = gevent.socket.gethostbyname(socket.gethostname())
        port = 9999
        announcer = Announcer('Test', '_salut_test._tcp', port)
        while not announcer.announced:
            gevent.sleep(0.05)

        callback = MagicMock()
        browser = Browser(
            'Test', '_salut_test._tcp',
            resolved_callback=callback.resolved)

        while not browser.resolved:
            gevent.sleep(0.05)
        callback.resolved.assert_called_once_with(ip, port)

        browser.stop()
        announcer.stop()

    def test_browse_unresolved_callback(self):
        announcer = Announcer('Test', '_salut_test._tcp', 9999)
        while not announcer.announced:
            gevent.sleep(0.05)

        callback = MagicMock()
        browser = Browser(
            'Test', '_salut_test._tcp',
            unresolved_callback=callback.unresolved)

        while not browser.resolved:
            gevent.sleep(0.05)

        announcer.stop()
        while announcer.announced:
            gevent.sleep(0.05)
        announcer = None

        while browser.resolved:
            gevent.sleep(0.05)
        callback.unresolved.assert_called_once()

        browser.stop()

    def test_unresolve_resolve(self):
        announcer = Announcer('Test', '_salut_test._tcp', 9999)
        while not announcer.announced:
            gevent.sleep(0.05)

        browser = Browser('Test', '_salut_test._tcp')
        while not browser.resolved:
            gevent.sleep(0.05)

        announcer.stop()
        while announcer.announced:
            gevent.sleep(0.05)
        announcer = None

        while browser.resolved:
            gevent.sleep(0.05)

        announcer = Announcer('Test', '_salut_test._tcp', 9999)
        while not announcer.announced:
            gevent.sleep(0.05)
        while not browser.resolved:
            gevent.sleep(0.05)

        browser.stop()
