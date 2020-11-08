
import pygame

from player import *


class Screen:
    def __init__(self, game):
        self.game = game

    def update(self, events):
        pass


class PlayScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.everything = pygame.sprite.RenderUpdates()

        self.containers = {}
        for alignment in ['PLAYER', 'ENEMY']:
            self.containers[alignment] = {}
            for obj_type in ['ENTITY', 'BULLET']:
                self.containers[alignment][obj_type] = pygame.sprite.Group()

        self.player = Player(
            self.get_containers('PLAYER', 'ENTITY'),
            self.get_containers('PLAYER', 'BULLET')
        )
        self.background = pygame.Surface(self.game.SIZE)

    def get_containers(self, alignment, obj_type):
        return (
            self.everything,
            self.containers[alignment][obj_type]
        )

    def update(self, events):
        self.everything.clear(self.game.screen, self.background)
        self.everything.update()
        display = self.everything.draw(self.game.screen)
        pygame.display.update(display)


class EndScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
