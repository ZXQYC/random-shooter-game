"""This module contains the player entity for the game"""

import pygame
import numpy as np

from sprite_library import Collider
from health import Health, InfiniteHealth, OneHealth, HealthBar
from bullets import LinearBullet
from utils import image_load, Difficulty


class Player(Collider):
    """The player entity for the game"""
    MOVE_SPEED = 20
    SHOOT_DELAY = 3
    BULLET_VELOCITY = np.array((0, -20))
    BULLET_DAMAGE = 1
    BULLET_SPAWN_OFFSET = np.array((0, -12))

    sprite_image = image_load('player.png')
    hitbox_image = image_load('player_hitbox.png')
    bullet_image = image_load('player_bullet.png')

    @staticmethod
    def health_from_difficulty(diff):
        """Creates the player's health, given the difficulty"""
        if diff == Difficulty.TRIVIAL:
            return InfiniteHealth()
        if diff == Difficulty.NORMAL:
            return Health(100, .1)
        if diff == Difficulty.HARD:
            return OneHealth()
        return None

    def __init__(self, play_screen, start, diff=Difficulty.NORMAL):
        """Creates the Player"""
        super().__init__(
            containers=play_screen.get_containers('PLAYER', 'ENTITY'),
            image=self.sprite_image,
            start=start,
            health=self.health_from_difficulty(diff),
            damage=.1,
            hitbox=self.hitbox_image
        )
        self.difficulty = diff
        self.play_screen = play_screen
        HealthBar(
            containers=play_screen.everything,
            health=self.health,
            size=np.array((160, 20)),
            start=np.array((100, 610)),
            border_size=2,
            color=(0, 255, 0)
        )
        self.next_shot = 0
        self.bullet_containers = play_screen.get_containers('PLAYER', 'BULLET')

    def update(self):
        """Does various things to update the player"""
        # check if game started yet
        if not self.play_screen.game_started:
            return

        # make movement towards cursor
        vec_move = np.array(pygame.mouse.get_pos())-self.vec
        dist = np.linalg.norm(vec_move)
        if dist > self.MOVE_SPEED:
            vec_move = vec_move * self.MOVE_SPEED / dist
        self.move_by(vec_move)

        # update health
        self.health.update()

        # shoot bullet if available
        if self.next_shot == 0:
            LinearBullet(
                containers=self.bullet_containers,
                image=self.bullet_image,
                start=self.vec + self.BULLET_SPAWN_OFFSET,
                damage=self.BULLET_DAMAGE,
                velocity=self.BULLET_VELOCITY
            )
            self.next_shot = self.SHOOT_DELAY
        self.next_shot -= 1

        # check for keypresses (X to die, Z to lose some health)
        pressed = pygame.key.get_pressed()
        if pressed[ord('x')]:
            self.health.die()
        if pressed[ord('z')]:
            self.health.take_damage(10)
