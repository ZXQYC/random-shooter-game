
import pygame
import numpy as np

from utils import *


def collide_mask(c1, c2):
    return pygame.sprite.collide_mask(c1, c2) is not None


class Collider(pygame.sprite.Sprite):
    def __init__(self, containers, health, image, damage):
        super().__init__(containers)
        self.health = health
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.damage = damage
        self.vec = np.array(self.rect.center)

    def get_hit(self, other):
        self.health.take_damage(other.damage)
        if self.health.dead():
            self.kill()

    def move_to(self, vec):
        cx, cy = self.rect.center
        self.rect.move_ip(int(vec[0]-cx), int(vec[1]-cy))
        self.vec = vec

    def move_by(self, vec):
        self.move_to(vec+self.vec)

    def is_on_screen(self):
        horizontal = segment_intersects(self.rect.left, self.rect.right, 0, WINDOW_SIZE[0])
        vertical = segment_intersects(self.rect.bottom, self.rect.top, 0, WINDOW_SIZE[1])
        return vertical and horizontal

    @staticmethod
    def collide(c1, c2):
        c1.get_hit(c2)
        c2.get_hit(c1)

    @staticmethod
    def collide_all(c1, c2s):
        sprite_list = pygame.sprite.spritecollide(c1, c2s, False, collide_mask)
        for c2 in sprite_list:
            Collider.collide(c1, c2)
