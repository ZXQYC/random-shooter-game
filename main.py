import math
import random
import sys
import pygame

from health import *


class Screen:
    def __init__(self, game):
        self.game = game

    def update(self, events):
        pass


class PlayScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.everything = pygame.sprite.RenderUpdates()
        Player.containers = self.everything
        self.player = Player()
        self.background = pygame.Surface(self.game.SIZE)

    def update(self, events):
        self.everything.clear(self.game.screen, self.background)
        self.everything.update()
        display = self.everything.draw(self.game.screen)
        pygame.display.update(display)


class EndScreen(Screen):
    def __init__(self, game):
        super().__init__(game)


class Game:
    FPS = 30
    SIZE = (640, 640)
    START_SCREEN = PlayScreen

    def __init__(self):
        self.scene = self.START_SCREEN(self)
        self.screen = None

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(Game.SIZE)
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
            self.scene.update(events)
            clock.tick(self.FPS)

    def set_screen(self, new_screen):
        self.scene = new_screen(self)


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

    def get_hit(self, other):
        self.health.take_damage(other.damage)
        if self.health.dead():
            self.kill()

    @staticmethod
    def collide(c1, c2):
        c1.get_hit(c2)
        c2.get_hit(c1)

    @staticmethod
    def collide_all(c1, c2s):
        slist = pygame.sprite.spritecollide(c1, c2s, False, collide_mask)
        for c2 in slist:
            Collider.collide(c1, c2)


class Player(Collider):
    containers = None
    MOVE_SPEED = 20
    sprite_image = pygame.image.load("sprites/player.png")

    def __init__(self):
        super().__init__(
            containers=self.containers,
            health=Health(100),
            image=self.sprite_image,
            damage=10
        )

    def update(self):
        nx, ny = pygame.mouse.get_pos()
        cx, cy = self.rect.center
        dx, dy = nx-cx, ny-cy
        dist = (dx*dx+dy*dy)**.5
        if dist > self.MOVE_SPEED:
            dx, dy = dx*self.MOVE_SPEED/dist, dy*self.MOVE_SPEED/dist
        self.rect.move_ip(dx, dy)


def main():
    Game().run()


if __name__ == "__main__":
    main()
