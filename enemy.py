
import random

import numpy as np
import pygame

from sprite_library import Collider
from health import Health, HealthBar
from utils import INF, rot_matrix
from bullets import LinearBullet, BouncingBullet


class AttackPattern:
    def __init__(self, enemy, total_frames):
        self.enemy = enemy
        self.play_screen = enemy.play_screen
        self.player = self.play_screen.player
        self.containers = self.play_screen.get_containers('ENEMY', 'BULLET')
        self.frame = 0
        self.total_frames = total_frames
        self.done = False

    def to_player_vector(self, start=None):
        if start is None:
            start = self.enemy.vec
        else:
            start = np.array(start)
        ans = self.player.vec - start
        return ans / np.linalg.norm(ans)

    def shoot(self):
        pass

    def frames_left(self):
        return self.total_frames - self.frame

    def update(self):
        self.shoot()
        self.frame += 1
        if self.frame >= self.total_frames:
            self.done = True


class NotAttackPattern(AttackPattern):
    def __init__(self, enemy):
        super().__init__(enemy, 60)


class BlarghAttackPattern(AttackPattern):
    BULLET_SPEED = 8

    def __init__(self, enemy):
        super().__init__(enemy, 300)

    def shoot(self):
        if self.frames_left() < 60:
            return
        to_player = self.to_player_vector()
        if self.frame % 5 == 0:
            LinearBullet(
                containers=self.containers,
                image=self.enemy.bullet_image_60px,
                start=self.enemy.vec,
                damage=40,
                velocity=to_player*self.BULLET_SPEED
            )
        if self.frame % 2 == 0:
            max_rot = np.pi / 3
            rand_theta = random.random() * 2 * max_rot - max_rot
            to_player_rand = rot_matrix(rand_theta) @ to_player
            LinearBullet(
                containers=self.containers,
                image=self.enemy.bullet_image_30px,
                start=self.enemy.vec,
                damage=20,
                velocity=to_player_rand * self.BULLET_SPEED
            )


class BounceAttackPattern(AttackPattern):
    BULLET_SPEED = 6

    def __init__(self, enemy):
        super().__init__(enemy, 300)

    def shoot(self):
        if self.frame < 60 and self.frame % 4 == 0:
            down = np.array([0, -1])
            max_rot = np.pi
            rand_theta = random.random() * 2 * max_rot - max_rot
            direction_rand = rot_matrix(rand_theta) @ down
            BouncingBullet(
                containers=self.containers,
                image=self.enemy.bullet_image_120px,
                start=self.enemy.vec,
                damage=80,
                velocity=direction_rand * self.BULLET_SPEED,
                max_bounce=self.total_frames-120
            )


class Enemy(Collider):
    sprite_image = pygame.image.load('sprites/enemy.png')
    pattern_list = [BounceAttackPattern]

    bullet_image_120px = pygame.image.load('sprites/enemy_bullet_120px.png')
    bullet_image_60px = pygame.image.load('sprites/enemy_bullet_60px.png')
    bullet_image_30px = pygame.image.load('sprites/enemy_bullet_30px.png')

    def __init__(self, play_screen, start):
        super().__init__(
            containers=play_screen.get_containers('ENEMY', 'ENTITY'),
            image=self.sprite_image,
            start=start,
            health=Health(100),
            damage=10
        )
        self.play_screen = play_screen
        HealthBar(
            containers=play_screen.everything,
            health=self.health,
            size=np.array((580, 30)),
            start=np.array((320, 45)),
            border_size=3,
            color=(255, 0, 0)
        )
        self.attack_pattern = None
        self.current_pattern = -1
        self.new_attack_pattern()

    def new_attack_pattern(self):
        new_index = self.current_pattern
        if len(self.pattern_list) > 1:
            while new_index == self.current_pattern:
                new_index = random.randrange(len(self.pattern_list))
        self.current_pattern = new_index
        self.attack_pattern = self.pattern_list[new_index](self)

    def update(self):
        # check if game started yet
        if not self.play_screen.game_started:
            return
        # update attack pattern
        if self.attack_pattern.done:
            self.new_attack_pattern()
        self.attack_pattern.update()
