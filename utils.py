"""Utility functions and constants for use elsewhere in the program"""

WINDOW_SIZE = (640, 640)


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
