"""The main menu for the game"""

import numpy as np

from sprite_library import TextSprite, Button
from screen import Screen
from utils import difficulties

import play_screen
import high_score_screen


class MainScreen(Screen):
    """The main menu"""
    def __init__(self, game):
        """Create the main menu"""
        super().__init__(game)

        # create title
        TextSprite(
            self.everything,
            "A RANDOM SHOOTER GAME",
            np.array((320, 120)),
            48
        )

        # create buttons for every difficulty
        for diff_i, diff in enumerate(difficulties):
            startx = np.array((120, 0)) + np.array((200, 0)) * diff_i
            size = np.array((180, 60))
            # create difficulty label
            TextSprite(
                self.everything,
                diff,
                startx+np.array((0, 200)),
                24
            )
            # create play game button
            to_play_screen = self.get_transition(
                play_screen.PlayScreen,
                diff
            )
            Button(
                containers=self.everything,
                text="PLAY GAME",
                start=startx + np.array((0, 280)),
                size=size,
                onclick=to_play_screen
            )
            # create high scores button
            to_high_score_screen = self.get_transition(
                high_score_screen.HighScoreScreen,
                diff
            )
            Button(
                containers=self.everything,
                text="HIGH SCORES",
                start=startx + np.array((0, 380)),
                size=size,
                onclick=to_high_score_screen
            )

    def get_transition(self, screen, diff):
        """Creates a transition function for a button to call when clicked"""
        return lambda: self.screen_transition(screen(self.game, diff))
