"""Tests week 3 functionality"""

import os
import unittest
from leaderboard import Leaderboard


class TestWeek3(unittest.TestCase):
    """Tests the game"""
    def test_db_valid(self):
        lb = Leaderboard('test')
        self.assertTrue(lb.valid)
        del os.environ['ATLAS_KEY']
        lb = Leaderboard('test')
        self.assertFalse(lb.valid)

    def test_db_insert(self):
        lb = Leaderboard('test')
        lb.clear_database()
        lb.add_score('TRIVIAL', 120, 'me')
        lb.add_score('NORMAL', 150, 'notme')
        val = lb.get_top('TRIVIAL')
        self.assertEqual(1, len(val))
        self.assertEqual(120, val[0]['time'])
        self.assertEqual('me', val[0]['name'])

    def test_db_top5(self):
        lb = Leaderboard('test')
        lb.clear_database()
        lb.add_score('HARD', 120, 'a')
        lb.add_score('HARD', 118, 'b')
        lb.add_score('HARD', 122, 'c')
        lb.add_score('HARD', -3, 'd')
        lb.add_score('HARD', -8, 'e')
        lb.add_score('HARD', 2, 'f')
        val = lb.get_top('HARD')
        self.assertEqual(5, len(val))
        self.assertEqual(-8, val[0]['time'])
        self.assertEqual(120, val[4]['time'])

    def test_db_is_high(self):
        lb = Leaderboard('test')
        lb.clear_database()
        self.assertTrue(lb.is_high_score('HARD', 99999999))
        lb.add_score('HARD', 120, 'a')
        lb.add_score('HARD', 118, 'b')
        lb.add_score('HARD', 122, 'c')
        lb.add_score('HARD', -3, 'd')
        self.assertTrue(lb.is_high_score('HARD', 99999999))
        lb.add_score('HARD', -8, 'e')
        self.assertFalse(lb.is_high_score('HARD', 99999999))
        lb.add_score('HARD', 2, 'f')
        self.assertTrue(lb.is_high_score('HARD', 119))
        self.assertFalse(lb.is_high_score('HARD', 120))
