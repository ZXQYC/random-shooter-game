"""The screen that displays high scores for the game"""

import numpy as np

from screens.screen import Screen
from sprite.sprite_library import TextSprite, Button
from utils import NAME_LEN, MAX_LEADERS

from screens import main_screen


def format_line(place, name, time):
    """Formats a single leaderboard line"""
    place_size = len(str(MAX_LEADERS))
    return '%s  %s  %s' % (
        str(place).rjust(place_size),
        name.ljust(NAME_LEN),
        str(time).ljust(8)
    )


class HighScoreScreen(Screen):
    """The high score screen"""
    def __init__(self, game, diff):
        """Create the high score screen"""
        super().__init__(game)
        self.diff = diff
        # display title
        TextSprite(
            self.everything,
            "LEADERBOARD",
            np.array((320, 80)),
            48
        )
        TextSprite(
            self.everything,
            "DIFFICULTY: "+diff,
            np.array((320, 140)),
            30
        )

        # display leaderboard
        lines = self.format_leaderboard()
        for place, line in enumerate(lines):
            TextSprite(
                self.everything,
                line,
                np.array((320, 200)) + np.array((0, 40)) * place,
                24
            )

        # button to return to main menu
        Button(
            self.everything,
            "MAIN MENU",
            np.array((320, 520)),
            np.array((200, 100)),
            lambda: self.screen_transition(main_screen.MainScreen(self.game))
        )

    def format_leaderboard(self):
        """Returns a list of string to be displayed as the leaderboard"""
        data = self.game.leaderboard.get_top(self.diff)
        ans = [format_line('#', 'NAME', 'TIME (S)')]
        for place in range(MAX_LEADERS):
            if place < len(data):
                ans.append(format_line(place+1, data[place]['name'], data[place]['time']))
            else:
                ans.append(format_line(place+1, '', '---'))
        return ans
