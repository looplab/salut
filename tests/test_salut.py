import unittest
from mock import MagicMock

import socket
import gevent
import gevent.socket

from otis.common.salut import Announcer, Browser


class TestSalut(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_announce(self):
        announcer = Announcer('Test', '_otis_test._tcp', 9999)

        while not announcer.announced:
            gevent.sleep(0.05)

        announcer.stop()

    def test_announce_registered_callback(self):
        callback = MagicMock()
        announcer = Announcer(
            'Test', '_otis_test._tcp', 9999, callback.registered)

        while not announcer.announced:
            gevent.sleep(0.05)
        callback.registered.assert_called_once_with(
            'local.', '_otis_test._tcp.', 'Test')

        announcer.stop()

    def test_browse(self):
        announcer = Announcer('Test', '_otis_test._tcp', 9999)
        while not announcer.announced:
            gevent.sleep(0.05)

        browser = Browser(
            'Test', '_otis_test._tcp')

        while not browser.resolved:
            gevent.sleep(0.05)

        browser.stop()
        announcer.stop()

    def test_browse_resolved_callback(self):
        ip = gevent.socket.gethostbyname(socket.gethostname())
        port = 9999
        announcer = Announcer('Test', '_otis_test._tcp', port)
        while not announcer.announced:
            gevent.sleep(0.05)

        callback = MagicMock()
        browser = Browser(
            'Test', '_otis_test._tcp',
            resolved_callback=callback.resolved)

        while not browser.resolved:
            gevent.sleep(0.05)
        callback.resolved.assert_called_once_with(ip, port)

        browser.stop()
        announcer.stop()

    def test_browse_unresolved_callback(self):
        announcer = Announcer('Test', '_otis_test._tcp', 9999)
        while not announcer.announced:
            gevent.sleep(0.05)

        callback = MagicMock()
        browser = Browser(
            'Test', '_otis_test._tcp',
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
        announcer = Announcer('Test', '_otis_test._tcp', 9999)
        while not announcer.announced:
            gevent.sleep(0.05)

        browser = Browser('Test', '_otis_test._tcp')
        while not browser.resolved:
            gevent.sleep(0.05)

        announcer.stop()
        while announcer.announced:
            gevent.sleep(0.05)
        announcer = None

        while browser.resolved:
            gevent.sleep(0.05)

        announcer = Announcer('Test', '_otis_test._tcp', 9999)
        while not announcer.announced:
            gevent.sleep(0.05)
        while not browser.resolved:
            gevent.sleep(0.05)

        browser.stop()
