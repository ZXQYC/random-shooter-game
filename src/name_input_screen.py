
import numpy as np
import pygame

from screen import Screen
from sprite_library import TextSprite, Button
from utils import NAME_LEN

import main_screen
import high_score_screen


class TextInputSprite(TextSprite):
    def __init__(self, screen, start, max_len):
        self.value = ''
        self.max_len = max_len
        super().__init__(
            containers=screen.everything,
            text=self.display_text(),
            start=start
        )
        self.screen = screen

    def display_text(self):
        return self.value.ljust(self.max_len, '_')

    def get_input(self):
        return self.value

    def update(self):
        for event in self.screen.events:
            if event.type == pygame.KEYDOWN:
                try:
                    key = chr(event.key)
                    if key.isalnum() and len(self.value) < self.max_len:
                        self.value += key
                except ValueError:
                    pass
                if event.key == pygame.K_BACKSPACE and len(self.value) > 0:
                    self.value = self.value[:-1]
                self.set_text(self.display_text())


class NameInputScreen(Screen):
    def __init__(self, game, diff, time):
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
        TextSprite(
            self.everything,
            'ENTER YOUR NAME:',
            np.array((320, 200)),
            30
        )
        self.text_input = TextInputSprite(
            self,
            np.array((320, 240)),
            NAME_LEN
        )
        Button(
            self.everything,
            "SUBMIT",
            np.array((320, 360)),
            np.array((200, 60)),
            self.submit
        )
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
        name = self.text_input.value
        self.game.leaderboard.add_score(self.diff, self.time, name)
        self.screen_transition(high_score_screen.HighScoreScreen(self.game, self.diff))

    def cancel(self):
        self.screen_transition(main_screen.MainScreen(self.game))
