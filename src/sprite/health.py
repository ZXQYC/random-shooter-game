"""Handles how much health bullets and entities have"""

import pygame

from sprite.sprite_library import RectangleSprite


class Health:
    """A normal health object that keeps track of maximum and remaining HP"""
    def __init__(self, hp=1, regen=0):
        """Creates the Health object"""
        self.max_hp = hp
        self.hp = hp
        self.regen = regen

    def take_damage(self, dmg):
        """Makes the object take dmg damage"""
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def dead(self):
        """Checks whether or not the object has died"""
        return self.hp == 0

    def die(self):
        """Kills the object"""
        self.hp = 0

    def update(self):
        """Regenerates health if not dead"""
        if not self.dead():
            self.hp = min(self.hp+self.regen, self.max_hp)


class InfiniteHealth(Health):
    """A version of Health that cannot die unless die() is invoked directly"""
    def take_damage(self, dmg):
        """Doesn't take damage"""


class OneHealth(Health):
    """A version of Health that dies instantly upon taking damage"""
    def take_damage(self, dmg):
        """Dies if damage is positive"""
        if dmg > 0:
            self.die()


class HealthBar(RectangleSprite):
    """A health bar sprite for a given Health object"""
    def __init__(self, containers, health, size, start, border_size=1, color=(1, 1, 1)):
        """Creates the health bar"""
        super().__init__(containers, (255, 255, 255), size, border_size, start)
        self.health = health
        self.inner_color = color

    def update(self):
        """Draws the health bar"""
        # drawing the image is done by 3 steps:
        # draw white (for border), draw black (for inside), draw self.color (for health)
        super().update()
        self.image.fill(self.inner_color, pygame.Rect(
            self.border_size,
            self.border_size,
            int(self.inner_size[0] * self.health.hp / self.health.max_hp),
            self.inner_size[1]
        ))
