
import pygame


class Health:
    def __init__(self, hp=1, regen=0):
        self.max_hp = hp
        self.hp = hp
        self.regen = regen

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def dead(self):
        return self.hp == 0

    def die(self):
        self.hp = 0

    def update(self):
        if not self.dead():
            self.hp = min(self.hp+self.regen, self.max_hp)


class InfiniteHealth(Health):
    def take_damage(self, dmg):
        pass


class OneHealth(Health):
    def take_damage(self, dmg):
        if dmg > 0:
            self.die()


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, containers, health, size, location, border_size=1, color=(1, 1, 1)):
        super().__init__(containers)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect().move(location[0], location[1])
        self.health = health
        self.border_size = border_size
        self.color = color
        self.size = size
        self.inner_size = size-2*border_size

    def update(self):
        # drawing the image is done by 3 steps:
        # draw white (for border), draw black (for inside), draw self.color (for health)
        self.image.fill((255, 255, 255))
        self.image.fill((0, 0, 0), pygame.Rect(
            self.border_size,
            self.border_size,
            self.inner_size[0],
            self.inner_size[1]
        ))
        self.image.fill(self.color, pygame.Rect(
            self.border_size,
            self.border_size,
            int(self.inner_size[0] * self.health.hp / self.health.max_hp),
            self.inner_size[1]
        ))
