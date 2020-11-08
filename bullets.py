"""All the bullets to be used in the game"""

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
