
import random

import numpy as np
import pygame

from sprite_library import Collider
from health import Health, HealthBar
from utils import INF, rot_matrix
from bullets import LinearBullet


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

    def update(self):
        self.shoot()
        self.frame += 1
        if self.frame >= self.total_frames:
            self.done = True


class NotAttackPattern(AttackPattern):
    def __init__(self, enemy):
        super().__init__(enemy, INF)


class BlarghAttackPattern(AttackPattern):
    BULLET_SPEED = 8

    def __init__(self, enemy):
        super().__init__(enemy, 300)

    def shoot(self):
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


class Enemy(Collider):
    sprite_image = pygame.image.load('sprites/enemy.png')
    pattern_list = [BlarghAttackPattern]

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
        self.new_attack_pattern()

    def new_attack_pattern(self):
        new_pattern = random.choice(self.pattern_list)
        self.attack_pattern = new_pattern(self)

    def update(self):
        # check if game started yet
        if not self.play_screen.game_started:
            return
        # update attack pattern
        if self.attack_pattern.done:
            self.new_attack_pattern()
        self.attack_pattern.update()
