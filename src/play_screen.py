"""The screen for playing a game"""

import time

import numpy as np
import pygame

from screen import Screen
from sprite_library import VectorSprite, TextSprite, RectangleSprite, Collider
from player import Player
from enemy import Enemy
from utils import time_str, image_load, Difficulty

import end_screen


class GameStartCircle(VectorSprite):
    """A circle used at the start of a game. Hover cursor inside to begin game."""
    circle_image = image_load('game_start_circle.png')

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
    ENEMY_START = np.array((320, 160))

    def __init__(self, game, diff=Difficulty.NORMAL):
        """Create the PlayScreen"""
        super().__init__(game)
        self.game_started = False
        self.game_ended = False
        self.game_won = False
        self.start_time = 0
        self.diff = diff

        # create containers
        self.containers = {}
        for alignment in ['PLAYER', 'ENEMY']:
            self.containers[alignment] = {}
            for obj_type in ['ENTITY', 'BULLET']:
                self.containers[alignment][obj_type] = pygame.sprite.Group()

        # create objects
        self.start_circle = GameStartCircle(self, self.PLAYER_START)
        self.player = Player(self, self.PLAYER_START, diff)
        self.start_text = TextSprite(
            self.everything,
            "Put your cursor in the circle to start the game!",
            (320, 330),
            16
        )
        self.time_text = TextSprite(
            self.everything,
            time_str(0),
            (570, 620),
            16
        )
        self.enemy = Enemy(self, self.ENEMY_START)

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

    def full_screen_rectangle(self, color):
        """Creates a full screen rectangle of a particular color"""
        RectangleSprite(
            self.everything,
            color,
            np.array((650, 650)),
            np.array((0, 0)),
            np.array((320, 320)),
            True
        )

    def update(self, events):
        """Updates the game screen"""
        super().update(events)
        # kill the start text if it already exists
        if self.game_started:
            self.start_text.kill()
            self.time_text.set_text(time_str(self.current_time()))

        # do collision detection
        Collider.collide_all(self.player, self.containers['ENEMY']['BULLET'])
        Collider.collide_all(self.enemy, self.containers['PLAYER']['BULLET'])
        Collider.collide_all(self.player, self.containers['ENEMY']['ENTITY'])

        # transition to end screen if game ended
        if self.game_ended:
            self.screen_transition(end_screen.EndScreen(
                self.game,
                self.game_won,
                self.current_time(),
                self.diff
            ))

        # if player is dead, get ready to screen transition next frame
        if self.player.health.dead():
            self.game_ended = True
            self.full_screen_rectangle((255, 0, 0))

        # if enemy is dead, also get ready to transition
        if self.enemy.health.dead():
            self.game_ended = True
            self.game_won = True
            self.full_screen_rectangle((255, 255, 255))
