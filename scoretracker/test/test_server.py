import unittest

from unittest import mock

from scoretracker import tracker


class FakeArgAll():
    json = {'text': '/score show'}
class FakeArgAllForOne():
    json = {'text': '/score show Ron'}
class FakeArgOneForOne():
    json = {'text': '/score show Ron Dissappointment'}
class FakeArgIncr():
    json = {'text': '/score Ron Dissappointment + 420'}

class TestServer(unittest.TestCase):
    @mock.patch('scoretracker.tracker.connexion.request', FakeArgAll)
    @mock.patch('scoretracker.tracker.show_score', return_value=None)
    def test_main_loop(self, shsc):
        tracker.recv_msg()
        shsc.assert_called_once_with()

    @mock.patch('scoretracker.tracker.connexion.request', FakeArgAllForOne)
    @mock.patch('scoretracker.tracker.show_score', return_value=None)
    def test_show_all_individual(self, shsc):
        tracker.recv_msg()
        shsc.assert_called_once_with('Ron')

    @mock.patch('scoretracker.tracker.connexion.request', FakeArgOneForOne)
    @mock.patch('scoretracker.tracker.show_score', return_value=None)
    def test_show_one_individual(self, shsc):
        tracker.recv_msg()
        shsc.assert_called_once_with('Ron', 'Dissappointment')

    @mock.patch('scoretracker.tracker.connexion.request', FakeArgIncr)
    @mock.patch('scoretracker.tracker.increment_score', return_value=None)
    def test_inc_score(self, incsc):
        tracker.recv_msg()
        incsc.assert_called_once_with('Dissappointment', 'Ron', 420)
