"""Utility functions and constants for use elsewhere in the program"""

import numpy as np
import pygame

WINDOW_SIZE = (640, 640)

INF = float('inf')

SPRITE_DIR = ['../sprites/', './sprites/']


def image_load(name):
    """Loads an image"""
    for directory in SPRITE_DIR:
        try:
            return pygame.image.load(directory + name)
        except FileNotFoundError:
            pass


def segment_intersects(pt1, pt2, xmin, xmax, threshold=1):
    """Checks whether or not the segment [pt1, pt2] intersects with [xmin, xmax]"""
    values = [(pt1, True), (pt2, True), (xmin - threshold, False), (xmax + threshold, False)]
    values.sort()
    return values[0][1] != values[1][1]


def time_str(secs, ljust=5):
    """Creates a time string to be displayed"""
    left = "Time: "
    right = str(int(secs))
    return (left+right).ljust(len(left)+ljust)


def rot_matrix(theta):
    """Creates the rotation matrix for a given rotation angle"""
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


class Difficulty:
    TRIVIAL = 'TRIVIAL'
    NORMAL = 'NORMAL'
    HARD = 'HARD'


difficulties = [Difficulty.TRIVIAL, Difficulty.NORMAL, Difficulty.HARD]
