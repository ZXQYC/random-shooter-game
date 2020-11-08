import math
import random
import sys
import pygame
import numpy as np

from health import *
from sprite_library import *
from player import *
from screen import *
from utils import *


class Game:
    FPS = 30
    SIZE = WINDOW_SIZE
    START_SCREEN = PlayScreen

    def __init__(self):
        self.scene = self.START_SCREEN(self)
        self.screen = None

    def run(self):
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(Game.SIZE)
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
            self.scene.update(events)
            clock.tick(self.FPS)

    def set_scene(self, new_screen):
        self.scene = new_screen


if __name__ == "__main__":
    pygame.init()
    Game().run()
