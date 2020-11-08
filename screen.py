"""Scenes for the game"""

import time
import sys

import pygame
import numpy as np

from sprite_library import VectorSprite, RectangleSprite, TextSprite, Button
from player import Player
from utils import time_str


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


class GameStartCircle(VectorSprite):
    """A circle used at the start of a game. Hover cursor inside to begin game."""
    circle_image = pygame.image.load('sprites/game_start_circle.png')

    def __init__(self, play_screen, start):
        """Create the circle"""
        super().__init__(play_screen.everything, self.circle_image, start)
        self.play_screen = play_screen

    def update(self):
        """If cursor is inside, start the game and die"""
        radius = self.rect.size[0]/2
        cursor_loc = np.array(pygame.mouse.get_pos())
        if np.linalg.norm(self.vec-cursor_loc) < radius:
            self.play_screen.start_game()
            self.kill()


class PlayScreen(Screen):
    """The screen for playing the game"""
    PLAYER_START = np.array((320, 400))

    def __init__(self, game):
        """Create the PlayScreen"""
        super().__init__(game)

        self.game_started = False
        self.game_ended = False
        self.start_time = 0

        # create containers
        self.containers = {}
        for alignment in ['PLAYER', 'ENEMY']:
            self.containers[alignment] = {}
            for obj_type in ['ENTITY', 'BULLET']:
                self.containers[alignment][obj_type] = pygame.sprite.Group()

        # create objects
        self.start_circle = GameStartCircle(self, self.PLAYER_START)
        self.player = Player(self, self.PLAYER_START)
        self.start_text = TextSprite(
            self.everything,
            "Put your cursor in the circle to start the game!",
            (320, 320),
            16
        )
        self.time_text = TextSprite(
            self.everything,
            time_str(0),
            (570, 620),
            16
        )

    def start_game(self):
        """Starts the game (called when player hovers over the start circle)"""
        self.game_started = True
        self.start_time = time.time()

    def current_time(self):
        """Returns the current play time, rounded to the nearest integer"""
        if not self.game_started:
            return 0
        return int(time.time()-self.start_time)

    def get_containers(self, alignment, obj_type):
        """Gets a particular container"""
        return (
            self.everything,
            self.containers[alignment][obj_type]
        )

    def update(self):
        """Updates the game screen"""
        super().update()
        # kill the start text if it already exists
        if self.game_started:
            self.start_text.kill()
            self.time_text.set_text(time_str(self.current_time()))

        # transition to end screen if game ended
        if self.game_ended:
            self.screen_transition(EndScreen(self.game, False, self.current_time()))

        # if player is dead, get ready to screen transition next frame
        if self.player.health.dead():
            self.game_ended = True
            RectangleSprite(
                self.everything,
                (255, 0, 0),
                np.array((650, 650)),
                np.array((0, 0)),
                np.array((320, 320)),
                True
            )


class EndScreen(Screen):
    """A screen for displaying results after a game"""
    LOSE_WIN_SIZE = 48
    LOSE_WIN_LOC = np.array((320, 180))

    def __init__(self, game, game_won, time_taken):
        """Creates the EndScreen"""
        super().__init__(game)
        # display either YOU WIN or YOU LOSE
        if game_won:
            TextSprite(
                self.everything,
                "YOU WIN",
                self.LOSE_WIN_LOC,
                self.LOSE_WIN_SIZE
            )
        else:
            TextSprite(
                self.everything,
                "YOU LOSE",
                self.LOSE_WIN_LOC,
                self.LOSE_WIN_SIZE,
                color=(255, 0, 0)
            )
        # display time taken
        TextSprite(
            self.everything,
            time_str(time_taken, 0),
            (320, 240)
        )
        # create a continue button
        Button(
            self.everything,
            "CONTINUE",
            np.array((320, 400)),
            np.array((200, 100)),
            sys.exit
        )
