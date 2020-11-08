"""Scenes for the game"""

import pygame


class Screen:
    """A generic screen"""
    def __init__(self, game):
        """Creates the screen"""
        self.game = game
        self.everything = pygame.sprite.RenderUpdates()
        self.background = pygame.Surface(self.game.SIZE)

    def update(self):
        """Updates the screen given certain events"""
        self.everything.clear(self.game.screen, self.background)
        self.everything.update()
        display = self.everything.draw(self.game.screen)
        pygame.display.update(display)

    def screen_transition(self, new_screen):
        """Transition to a different screen"""
        self.everything.clear(self.game.screen, self.background)
        self.game.set_scene(new_screen)
