"""Tests game functionality"""

import unittest
from utils import segment_intersects, time_str
from sprite.health import Health, InfiniteHealth, OneHealth


class TestWeek1(unittest.TestCase):
    """Tests the game"""
    def test_segment_intersects(self):
        res = segment_intersects(1, 5, 4, 6)
        self.assertTrue(res)
        res = segment_intersects(1, 2, 4, 6)
        self.assertFalse(res)
        res = segment_intersects(1, 9, 4, 6)
        self.assertTrue(res)

    def test_segment_intersects_threshold(self):
        res = segment_intersects(1, 4, 4, 6, threshold=1)
        self.assertTrue(res)
        res = segment_intersects(6, 8, 1, 5, threshold=2)
        self.assertTrue(res)
        res = segment_intersects(1, 3, 4, 6, threshold=0)
        self.assertFalse(res)

    def test_time_str(self):
        res = time_str(0)
        self.assertEqual("Time: 0    ", res)
        res = time_str(142)
        self.assertEqual("Time: 142  ", res)

    def test_time_str_no_ljust(self):
        res = time_str(0, ljust=0)
        self.assertEqual("Time: 0", res)
        res = time_str(142, ljust=0)
        self.assertEqual("Time: 142", res)

    def test_health_init(self):
        res = Health(100, regen=1)
        self.assertEqual(100, res.max_hp)
        self.assertEqual(100, res.hp)
        self.assertEqual(1, res.regen)

    def test_health_damage(self):
        res = Health(100, regen=1)
        res.take_damage(20)
        self.assertEqual(100, res.max_hp)
        self.assertEqual(80, res.hp)
        self.assertFalse(res.dead())

    def test_health_dead(self):
        res = Health(100, regen=1)
        res.take_damage(120)
        self.assertEqual(100, res.max_hp)
        self.assertEqual(0, res.hp)
        self.assertTrue(res.dead())

    def test_health_regen(self):
        res = Health(100, regen=1)
        res.take_damage(20)
        res.update()
        self.assertEqual(100, res.max_hp)
        self.assertEqual(81, res.hp)
        self.assertFalse(res.dead())

    def test_health_regen_while_dead(self):
        res = Health(100, regen=1)
        res.take_damage(120)
        res.update()
        self.assertEqual(0, res.hp)
        self.assertTrue(res.dead())

    def test_one_health(self):
        res = OneHealth()
        res.take_damage(0.1)
        self.assertEqual(1, res.max_hp)
        self.assertEqual(0, res.hp)
        self.assertTrue(res.dead())

    def test_infinite_health(self):
        res = InfiniteHealth()
        res.take_damage(9999999999999999)
        self.assertEqual(1, res.hp)
        self.assertFalse(res.dead())

    def test_unignorable_die(self):
        res = InfiniteHealth()
        res.die()
        self.assertEqual(0, res.hp)
        self.assertTrue(res.dead())
