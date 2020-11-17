"""The screen for display game results"""

import numpy as np

from screen import Screen
from sprite_library import TextSprite, Button
from utils import time_str

import play_screen


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
            self.to_play_screen
        )

    def to_play_screen(self):
        """Goes to the play screen"""
        self.screen_transition(play_screen.PlayScreen(self.game))
