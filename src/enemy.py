"""The enemy for the game"""

import random

import numpy as np
import pygame

from sprite_library import Collider
from health import Health, HealthBar
from utils import image_load, rot_matrix
from bullets import LinearBullet, BouncingBullet, BombBullet


class AttackPattern:
    """An attack pattern that the enemy can use"""
    def __init__(self, enemy, total_frames):
        """Creates the attack pattern"""
        self.enemy = enemy
        self.play_screen = enemy.play_screen
        self.player = self.play_screen.player
        self.containers = self.play_screen.get_containers('ENEMY', 'BULLET')
        self.frame = 0
        self.total_frames = total_frames
        self.done = False

    def to_player_vector(self, start=None):
        """Creates a unit vector pointing from the given point to the player.
        If no given point, use the enemy's current position"""
        if start is None:
            start = self.enemy.vec
        else:
            start = np.array(start)
        ans = self.player.vec - start
        return ans / np.linalg.norm(ans)

    def shoot(self):
        """A function to be implemented in subclasses. Called once per frame."""

    def frames_left(self):
        """The number of frames left before the attack pattern ends"""
        return self.total_frames - self.frame

    def update(self):
        """Updates the attack pattern for a new frame"""
        self.shoot()
        self.frame += 1
        if self.frame >= self.total_frames:
            self.done = True


class NotAttackPattern(AttackPattern):
    """A fake attack pattern that doesn't do anything. Lasts 60 frames. """
    def __init__(self, enemy):
        """Creates the fake attack pattern"""
        super().__init__(enemy, 60)


class BlarghAttackPattern(AttackPattern):
    """An attack pattern that vomits bullets towards the player"""
    BULLET_SPEED = 8

    def __init__(self, enemy):
        """Creates the blargh attack pattern"""
        super().__init__(enemy, 300)

    def shoot(self):
        """Shoots bullets at the player"""
        # do nothing if there is less than 60 frames left
        if self.frames_left() < 60:
            return
        to_player = self.to_player_vector()
        # Shoot a 60px bullet at the player every 4 frames
        if self.frame % 4 == 0:
            LinearBullet(
                containers=self.containers,
                image=self.enemy.bullet_image_60px,
                start=self.enemy.vec,
                damage=50,
                velocity=to_player*self.BULLET_SPEED
            )
        # Shoot two 30px bullets near the player every 2 frames
        if self.frame % 2 == 0:
            max_rot = np.pi / 2
            rand_theta = random.random() * 2 * max_rot - max_rot
            to_player_rand = rot_matrix(rand_theta) @ to_player
            LinearBullet(
                containers=self.containers,
                image=self.enemy.bullet_image_30px,
                start=self.enemy.vec,
                damage=40,
                velocity=to_player_rand * self.BULLET_SPEED
            )
            max_rot = np.pi / 4
            rand_theta = random.random() * 2 * max_rot - max_rot
            to_player_rand = rot_matrix(rand_theta) @ to_player
            LinearBullet(
                containers=self.containers,
                image=self.enemy.bullet_image_30px,
                start=self.enemy.vec,
                damage=40,
                velocity=to_player_rand * self.BULLET_SPEED
            )


class BounceAttackPattern(AttackPattern):
    """An attack pattern that shoots big bouncing bullets everywhere"""
    BULLET_SPEED = 6

    def __init__(self, enemy):
        """Creates the BounceAttackPattern"""
        super().__init__(enemy, 300)

    def shoot(self):
        """Shoots the bouncy bullets"""
        if self.frame < 60 and self.frame % 4 == 0:
            # Should shoot 15 bouncy bullets in 1 second, then stop doing anything
            down = np.array([0, 1])
            max_rot = np.pi
            rand_theta = random.random() * 2 * max_rot - max_rot
            direction_rand = rot_matrix(rand_theta) @ down
            BouncingBullet(
                containers=self.containers,
                image=self.enemy.bullet_image_120px,
                start=self.enemy.vec,
                damage=70,
                velocity=direction_rand * self.BULLET_SPEED,
                max_bounce=self.total_frames-120
            )


class BombAttackPattern(AttackPattern):
    """An attack pattern that throws bombs towards the bottom of the screen"""
    BULLET_SPEED = 6

    def __init__(self, enemy):
        """Creates the BombAttackPattern"""
        super().__init__(enemy, 300)

    def bomb_explode(self, start):
        """The function to be called when the bomb explodes"""
        down = np.array([0, 1])
        max_rot = np.pi
        rand_theta = random.random() * 2 * max_rot - max_rot
        num_bullets = 12
        for i in range(num_bullets):
            direction = rot_matrix(rand_theta+2*np.pi/num_bullets*i) @ down
            LinearBullet(
                containers=self.containers,
                image=self.enemy.bullet_image_60px,
                start=start + direction * 30,
                damage=50,
                velocity=direction * self.BULLET_SPEED
            )

    def shoot(self):
        """Shoots bombs towards the bottom of the screen"""
        if self.frame < 120 and self.frame % 6 == 0:
            # should fire 20 bombs in 2 seconds, then do nothing
            down = np.array([0, 1])
            max_rot = np.pi/6
            rand_theta = random.random() * 2 * max_rot - max_rot
            direction_rand = rot_matrix(rand_theta) @ down
            BombBullet(
                containers=self.containers,
                image=self.enemy.bomb_image_120px,
                start=self.enemy.vec,
                damage=50,
                velocity=direction_rand * self.BULLET_SPEED,
                on_explode=self.bomb_explode
            )


class Enemy(Collider):
    """The big bad evil guy"""
    pattern_list = [BlarghAttackPattern, BounceAttackPattern, BombAttackPattern]

    sprite_image = image_load('enemy.png')

    bomb_image_120px = image_load('enemy_bomb_120px.png')
    bullet_image_120px = image_load('enemy_bullet_120px.png')
    bullet_image_60px = image_load('enemy_bullet_60px.png')
    bullet_image_30px = image_load('enemy_bullet_30px.png')

    def __init__(self, play_screen, start):
        """Creates the enemy"""
        super().__init__(
            containers=play_screen.get_containers('ENEMY', 'ENTITY'),
            image=self.sprite_image,
            start=start,
            health=Health(400),
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
        """Switches to a new attack pattern"""
        new_index = self.current_pattern
        if len(self.pattern_list) > 1:
            while new_index == self.current_pattern:
                new_index = random.randrange(len(self.pattern_list))
        self.current_pattern = new_index
        self.attack_pattern = self.pattern_list[new_index](self)

    def update(self):
        """Updates the enemy"""
        # check if game started yet
        if not self.play_screen.game_started:
            return

        # update attack pattern
        if self.attack_pattern.done:
            self.new_attack_pattern()
        self.attack_pattern.update()

        # check for keypress to cheat and win
        pressed = pygame.key.get_pressed()
        if pressed[ord('y')]:
            self.health.die()
