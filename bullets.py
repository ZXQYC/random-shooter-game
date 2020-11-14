"""All the bullets to be used in the game"""

import numpy as np

from sprite_library import Collider
from health import OneHealth


class Bullet(Collider):
    """A generic bullet that does not move"""
    def __init__(self, containers, image, start, damage):
        """Creates the bullet"""
        super().__init__(containers, image, start, OneHealth(), damage)

    def update(self):
        """Destroys the bullet if it is off screen"""
        if not self.is_on_screen():
            self.kill()


class LinearBullet(Bullet):
    """An implementation of Bullet that moves in a line"""
    def __init__(self, containers, image, start, damage, velocity):
        """Creates the bullet"""
        super().__init__(containers, image, start, damage)
        self.vel = velocity

    def update(self):
        """Moves the bullet"""
        super().update()
        self.move_by(self.vel)


class BouncingBullet(LinearBullet):
    """A linear bullet that bounces when it hits the edge of the screen"""
    def __init__(self, containers, image, start, damage, velocity, max_bounce):
        super().__init__(containers, image, start, damage, velocity)
        self.max_bounce = max_bounce
        self.frame = 0

    def update(self):
        """Bounces the bullet if necessary"""
        super().update()
        if self.frame < self.max_bounce:
            boundaries = self.hitting_screen_boundary()
            for dimension in range(2):
                if boundaries[dimension]:
                    self.vel[dimension] = abs(self.vel[dimension]) * -boundaries[dimension]
        self.frame += 1


class BombBullet(LinearBullet):
    """A bullet that explodes when it is destroyed, or when it hits the edge of the screen"""
    def __init__(self, containers, image, start, damage, velocity, on_explode):
        super().__init__(containers, image, start, damage, velocity)
        self.on_explode = on_explode
        self.exploded = False

    def explode(self):
        """Causes the explosion"""
        if self.exploded:
            return
        self.exploded = True
        self.on_explode(self.vec)
        self.kill()

    def get_hit(self, other):
        """Explode the bullet when hit"""
        super().get_hit(other)
        self.explode()

    def update(self):
        """Explodes the bullet if necessary"""
        super().update()
        boundaries = self.center_off_screen()
        if np.linalg.norm(boundaries) > 0:
            self.explode()
