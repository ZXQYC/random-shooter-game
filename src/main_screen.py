"""The main menu for the game"""

import numpy as np

from sprite_library import TextSprite, Button
from screen import Screen
from utils import difficulties

import play_screen


class MainScreen(Screen):
    """The main menu"""
    def __init__(self, game):
        """Create the main menu"""
        super().__init__(game)
        TextSprite(
            self.everything,
            "A Random Shooter Game",
            np.array((320, 160)),
            36
        )
        for diff_i in range(len(difficulties)):
            Button(
                containers=self.everything,
                text="PLAY",
                start=np.array((160, 280)) + np.array((160, 0)) * diff_i,
                size=np.array((100, 80)),
                onclick=self.get_transition(play_screen.PlayScreen, difficulties[diff_i])
            )

    def get_transition(self, screen, diff):
        return lambda: self.screen_transition(screen(self.game, diff))
