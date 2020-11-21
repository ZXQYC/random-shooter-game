
import unittest
import numpy as np
import pygame

from utils import rot_matrix, INF
from sprite.sprite_library import VectorSprite
from sprite.bullets import BouncingBullet, BombBullet


class TestWeek2(unittest.TestCase):
    def test_rot_matrix_identity(self):
        self.assertEqual(np.identity(2).tolist(), rot_matrix(0).tolist())

    def test_rot_matrix(self):
        rot = rot_matrix(np.pi/2)
        self.assertAlmostEqual(0, rot[0, 0])
        self.assertAlmostEqual(-1, rot[0, 1])
        self.assertAlmostEqual(1, rot[1, 0])
        self.assertAlmostEqual(0, rot[1, 1])

    def test_hitting_screen_boundary_on_boundary(self):
        vs = VectorSprite(
            (),
            pygame.Surface((1, 1)),
            np.array((1, 1))
        )
        hsb = vs.hitting_screen_boundary().tolist()
        self.assertEqual([0, 0], hsb)

    def test_hitting_screen_boundary_off_boundary(self):
        vs = VectorSprite(
            (),
            pygame.Surface((200, 1)),
            np.array((600, -1))
        )
        hsb = vs.hitting_screen_boundary().tolist()
        self.assertEqual([1, -1], hsb)

    def test_center_off_screen_boundary(self):
        vs = VectorSprite(
            (),
            pygame.Surface((200, 8)),
            np.array((600, 0))
        )
        cos = vs.center_off_screen().tolist()
        self.assertEqual([0, 0], cos)

    def test_center_off_screen_really_off(self):
        vs = VectorSprite(
            (),
            pygame.Surface((1, 1)),
            np.array((640, -1))
        )
        cos = vs.center_off_screen().tolist()
        self.assertEqual([1, -1], cos)

    def test_bouncing_bullet(self):
        bb = BouncingBullet(
            containers=(),
            image=pygame.Surface((1, 1)),
            start=np.array((0, 1)),
            damage=0,
            velocity=np.array((-1, 0)),
            max_bounce=INF
        )
        bb.update()
        self.assertEqual([1, 0], bb.vel.tolist())
        self.assertEqual([-1, 1], bb.vec.tolist())

    def test_bomb_bullet(self):
        lst = []
        bb = BombBullet(
            containers=(),
            image=pygame.Surface((1, 1)),
            start=np.array((0, 0)),
            damage=0,
            velocity=np.array((-1, 1)),
            on_explode=lambda start: lst.append(start)
        )
        bb.update()
        self.assertTrue(bb.exploded)
        self.assertEqual([-1, 1], lst[0].tolist())
