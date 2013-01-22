Introduction
============

Salut is a Gevent based wrapper around the pybonjour library to facilitate
the use of bonjour in a cleaner way.

Salut is composed of two main classes, the Announcer and the Browser. Each have
a set of callbacks to respond to events without locking the main greenlet.


Example
=======

```python
class AnnouncerExample(object):
    def run(self):
        self._announcer = salut.Announcer(
            'ServiceName',
            '_regtype._tcp',
            5000,
            self._registered_callback)

        while True:
            gevent.sleep(1)

    def stop(self):
        self._announcer.stop()

    def _registered_callback(self, domain, regtype, name):
        print('announcing: %s%s%s' % (domain, regtype, name))
```

```python
class BrowseExample(object):
    def run(self):
        self._browser = salut.Browser(
            'ServiceName',
            '_regtype._tcp',
            self._resolved_callback,
            self._unresolved_callback)

        while True:
            gevent.sleep(1)

    def stop(self):
        self._browser.stop()

    def _resolved_callback(self, ip, port):
        print('resolved service to %s:%s' % (ip, port))

    def _unresolved_callback(self):
        print('lost service %s' % self._service_name)

```


License
=======

Salut is licensed under Apache License 2.0

http://www.apache.org/licenses/LICENSE-2.0
