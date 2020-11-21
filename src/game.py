"""The main game program"""

import sys

import pygame

from screens.main_screen import MainScreen
from utils import WINDOW_SIZE
from leaderboard import Leaderboard


class Game:
    """Controls the main game loop"""
    FPS = 30
    SIZE = WINDOW_SIZE

    def __init__(self):
        """Creates the Game object"""
        self.scene = MainScreen(self)
        self.screen = None
        self.leaderboard = Leaderboard()

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
            self.scene.update(events)
            clock.tick(self.FPS)

    def set_scene(self, new_screen):
        """Changes the scene the game is in"""
        self.scene = new_screen
