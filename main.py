import math
import random
import sys
import pygame


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
        Player()
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
        #self.rect = pygame.Rect(0, 0, Game.SIZE[0], Game.SIZE[1])
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


class Player(pygame.sprite.Sprite):
    containers = None
    MOVE_SPEED = 20

    def __init__(self):
        super().__init__(self.containers)
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()

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
