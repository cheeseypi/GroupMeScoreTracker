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

@mock.patch('builtins.open', mock.mock_open(read_data='{"Ron": {"Dissappointment": 420}}'))
@mock.patch('scoretracker.tracker.requests.post', return_value=None)
class TestServer(unittest.TestCase):
    @mock.patch('scoretracker.tracker.connexion.request', FakeArgAll)
    def test_main_loop(self, rpost):
        tracker.recv_msg()
        try:
            rpost.assert_called_once_with(tracker.POST_URL, '{"text": "Ron: \\n    Dissappointment: 420\\n", "bot_id": "TestID"}')
        except AssertionError:
            rpost.assert_called_once_with(tracker.POST_URL, '{"bot_id": "TestID", "text": "Ron: \\n    Dissappointment: 420\\n"}')

    @mock.patch('scoretracker.tracker.connexion.request', FakeArgAllForOne)
    def test_show_all_individual(self, rpost):
        tracker.recv_msg()
        try:
            rpost.assert_called_once_with(tracker.POST_URL, '{"text": "Dissappointment: 420\\n", "bot_id": "TestID"}')
        except AssertionError:
            rpost.assert_called_once_with(tracker.POST_URL, '{"bot_id": "TestID", "text": "Dissappointment: 420\\n"}')

    @mock.patch('scoretracker.tracker.connexion.request', FakeArgOneForOne)
    def test_show_one_individual(self, rpost):
        tracker.recv_msg()
        try:
            rpost.assert_called_once_with(tracker.POST_URL, '{"text": "Ron:\\n    Dissappointment: 420", "bot_id": "TestID"}')
        except AssertionError:
            rpost.assert_called_once_with(tracker.POST_URL, '{"bot_id": "TestID", "text": "Ron:\\n    Dissappointment: 420"}')

    @mock.patch('scoretracker.tracker.connexion.request', FakeArgIncr)
    def test_inc_score(self, rpost):
        tracker.recv_msg()
        try:
            rpost.assert_called_once_with(tracker.POST_URL, '{"text": "Incremented Dissappointment score by 420 for Ron", "bot_id": "TestID"}')
        except AssertionError:
            rpost.assert_called_once_with(tracker.POST_URL, '{"bot_id": "TestID", "text": "Incremented Dissappointment score by 420 for Ron"}')
