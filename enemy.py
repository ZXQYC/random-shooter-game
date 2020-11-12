
import random

import numpy as np
import pygame

from sprite_library import Collider
from health import Health, HealthBar
from utils import INF


class AttackPattern:
    def __init__(self, enemy, total_frames):
        self.enemy = enemy
        self.play_screen = enemy.play_screen
        self.player = self.play_screen.player
        self.frame = 0
        self.total_frames = total_frames
        self.done = False

    def update(self):
        self.frame += 1
        if self.frame >= self.total_frames:
            self.done = True


class NotAttackPattern(AttackPattern):
    def __init__(self, enemy):
        super().__init__(enemy, INF)


class Enemy(Collider):
    sprite_image = pygame.image.load('sprites/enemy.png')
    pattern_list = [NotAttackPattern]

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
        self.bullet_containers = play_screen.get_containers('ENEMY', 'BULLET')
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
