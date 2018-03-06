import unittest

from unittest import mock

from scoretracker import tracker

class TestServer(unittest.TestCase):
    @mock.patch('connexion.request.json', side_effect={'text': '/score show'})
    @mock.patch('scoretracker.tracker.show_score', return_value=None)
    def test_main_loop(self, shsc, connreq):
        shsc.assert_called_once_with()

    def test_show_all(self):
        return True

    def test_show_all_individual(self):
        return True

    def test_show_one_individual(self):
        return True

    def test_inc_score(self):
        return True
