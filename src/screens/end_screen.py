"""The screen for display game results"""

import numpy as np

from screens.screen import Screen
from sprite.sprite_library import TextSprite, Button
from utils import time_str

from screens import name_input_screen, main_screen


class EndScreen(Screen):
    """A screen for displaying results after a game"""
    LOSE_WIN_SIZE = 48
    LOSE_WIN_LOC = np.array((320, 180))

    def __init__(self, game, game_won, time_taken, diff):
        """Creates the EndScreen"""
        super().__init__(game)

        self.game_won = game_won
        self.time_taken = time_taken
        self.diff = diff

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
            self.next_screen
        )

    def next_screen(self):
        """Go to the next screen, depending on what happened in the game"""
        # if the game was won and the time is a high score, go to name input
        if self.game_won and self.game.leaderboard.is_high_score(self.diff, self.time_taken):
            self.screen_transition(
                name_input_screen.NameInputScreen(
                    self.game,
                    self.diff,
                    self.time_taken
                )
            )
        # otherwise, go back to main menu
        else:
            self.screen_transition(
                main_screen.MainScreen(self.game)
            )
