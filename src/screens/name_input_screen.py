"""The name input screen for the game"""

import numpy as np
import pygame

from screens.screen import Screen
from sprite.sprite_library import TextSprite, Button
from utils import NAME_LEN

from screens import high_score_screen, main_screen


class TextInputSprite(TextSprite):
    """A sprite that listens to keyboard input and acts as an input field"""
    def __init__(self, screen, start, max_len):
        """Initializes the text input sprite"""
        self.value = ''
        self.max_len = max_len
        super().__init__(
            containers=screen.everything,
            text=self.display_text(),
            start=start
        )
        self.screen = screen

    def display_text(self):
        """Generates the text to be displayed"""
        return self.value.ljust(self.max_len, '_')

    def update(self):
        """Updates the text, based on keydown events"""
        for event in self.screen.events:
            if event.type == pygame.KEYDOWN:
                # check for entering a valid char
                try:
                    key = chr(event.key)
                    if key.isalnum() and len(self.value) < self.max_len:
                        self.value += key
                except ValueError:
                    pass
                # check for backspace
                if event.key == pygame.K_BACKSPACE and len(self.value) > 0:
                    self.value = self.value[:-1]
                # update displayed text
                self.set_text(self.display_text())


class NameInputScreen(Screen):
    """The screen for allowing a player to enter their name"""
    def __init__(self, game, diff, time):
        """Creates the name input screen"""
        super().__init__(game)
        self.diff = diff
        self.time = time

        # create title
        TextSprite(
            self.everything,
            "HIGH SCORE!",
            np.array((320, 80)),
            48
        )

        # create instructions
        TextSprite(
            self.everything,
            'ENTER YOUR NAME:',
            np.array((320, 200)),
            30
        )

        # create text input field
        self.text_input = TextInputSprite(
            self,
            np.array((320, 240)),
            NAME_LEN
        )

        # create submit button
        Button(
            self.everything,
            "SUBMIT",
            np.array((320, 360)),
            np.array((200, 60)),
            self.submit
        )

        # create cancel button
        Button(
            self.everything,
            "CANCEL",
            np.array((320, 480)),
            np.array((200, 60)),
            self.cancel,
            color=(160, 0, 0),
            hover_color=(255, 0, 0)
        )

    def submit(self):
        """Submits the high score, going to the leaderboard"""
        name = self.text_input.value
        self.game.leaderboard.add_score(self.diff, self.time, name)
        self.screen_transition(high_score_screen.HighScoreScreen(self.game, self.diff))

    def cancel(self):
        """Cancels the high score, returning to the main menu"""
        self.screen_transition(main_screen.MainScreen(self.game))
