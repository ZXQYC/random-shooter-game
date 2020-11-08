
import pygame
import time

from player import *


class Screen:
    def __init__(self, game):
        self.game = game
        self.everything = pygame.sprite.RenderUpdates()
        self.background = pygame.Surface(self.game.SIZE)

    def update(self, events):
        self.everything.clear(self.game.screen, self.background)
        self.everything.update()
        display = self.everything.draw(self.game.screen)
        pygame.display.update(display)

    def screen_transition(self, new_screen):
        self.everything.clear(self.game.screen, self.background)
        self.game.set_scene(new_screen)


class GameStartCircle(VectorSprite):
    circle_image = pygame.image.load('sprites/game_start_circle.png')

    def __init__(self, play_screen, start):
        super().__init__(play_screen.everything, self.circle_image, start)
        self.play_screen = play_screen

    def update(self):
        radius = self.rect.size[0]/2
        cursor_loc = np.array(pygame.mouse.get_pos())
        if np.linalg.norm(self.vec-cursor_loc) < radius:
            self.play_screen.start_game()
            self.kill()


def time_str(secs):
    left = "Time: "
    right = str(int(secs))
    return (left+right).ljust(len(left)+5)


class PlayScreen(Screen):
    PLAYER_START = np.array((320, 400))

    def __init__(self, game):
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
        self.game_started = True
        self.start_time = time.time()

    def current_time(self):
        if not self.game_started:
            return 0
        else:
            return int(time.time()-self.start_time)

    def get_containers(self, alignment, obj_type):
        return (
            self.everything,
            self.containers[alignment][obj_type]
        )

    def update(self, events):
        super().update(events)
        # kill the start text if it already exists
        if self.game_started:
            self.start_text.kill()
            self.time_text.set_text(time_str(self.current_time()))

        # transition to end screen if game ended
        if self.game_ended:
            self.screen_transition(EndScreen(self.game, False, self.current_time()))

        if self.player.health.dead():
            self.game_ended = True





class EndScreen(Screen):
    LOSE_WIN_SIZE = 48
    LOSE_WIN_LOC = (320, 180)

    def __init__(self, game, game_won, time_taken):
        super().__init__(game)
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
        Button(
            self.everything,
            "CONTINUE",
            np.array((320, 400)),
            np.array((200, 100)),
            lambda: print("pressed!"),

        )
