"""The main game program"""

import sys

import pygame

from play_screen import PlayScreen
from utils import WINDOW_SIZE


class Game:
    """Controls the main game loop"""
    FPS = 30
    SIZE = WINDOW_SIZE
    START_SCREEN = PlayScreen

    def __init__(self):
        """Creates the Game object"""
        self.scene = self.START_SCREEN(self)
        self.screen = None

    def run(self):
        """Runs the game"""
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(Game.SIZE)
        while True:
            # check if game has been exited
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
            # update window and use clock tick
            self.scene.update()
            clock.tick(self.FPS)

    def set_scene(self, new_screen):
        """Changes the scene the game is in"""
        self.scene = new_screen


if __name__ == "__main__":
    pygame.init()
    Game().run()
