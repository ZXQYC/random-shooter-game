
from collider import *
from health import *


class Bullet(Collider):
    def __init__(self, containers, image, damage, start_loc):
        super().__init__(containers, OneHealth(), image, damage)
        '''self.started = False
        self.start_loc = start_loc'''
        self.move_to(start_loc)

    def update(self):
        '''if not self.started:
            self.started = True
            self.move_to(self.start_loc)
            print(self.start_loc)'''
        if not self.is_on_screen():
            return
            self.kill()


class LinearBullet(Bullet):
    def __init__(self, containers, image, damage, start_loc, velocity):
        super().__init__(containers, image, damage, start_loc)
        self.vel = velocity

    def update(self):
        super().update()
        self.move_by(self.vel)
