
from sprite_library import *
from health import *


class Bullet(Collider):
    def __init__(self, containers, image, start, damage):
        super().__init__(containers, image, start, OneHealth(), damage)

    def update(self):
        if not self.is_on_screen():
            self.kill()


class LinearBullet(Bullet):
    def __init__(self, containers, image, start, damage, velocity):
        super().__init__(containers, image, start, damage)
        self.vel = velocity

    def update(self):
        super().update()
        self.move_by(self.vel)
