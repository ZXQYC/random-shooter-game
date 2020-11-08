
from collider import *
from health import *
from bullets import *


class Player(Collider):
    MOVE_SPEED = 20
    SHOOT_DELAY = 3
    BULLET_VELOCITY = np.array((0, -20))
    BULLET_DAMAGE = 1
    BULLET_SPAWN_LOC = np.array((0, -12))
    sprite_image = pygame.image.load('sprites/player.png')
    bullet_image = pygame.image.load('sprites/player_bullet.png')

    def __init__(self, containers, bullet_containers):
        super().__init__(
            containers=containers,
            health=Health(100),
            image=self.sprite_image,
            damage=10
        )
        self.next_shot = 0
        self.bullet_containers = bullet_containers

    def update(self):
        vec_move = np.array(pygame.mouse.get_pos())-self.vec
        dist = np.linalg.norm(vec_move)
        if dist > self.MOVE_SPEED:
            vec_move = vec_move * self.MOVE_SPEED / dist
        self.move_by(vec_move)

        if self.next_shot == 0:
            LinearBullet(
                self.bullet_containers,
                self.bullet_image,
                self.BULLET_DAMAGE,
                self.vec+self.BULLET_SPAWN_LOC,
                self.BULLET_VELOCITY
            )
            self.next_shot = self.SHOOT_DELAY
        self.next_shot -= 1
