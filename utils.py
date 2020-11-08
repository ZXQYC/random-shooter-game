
WINDOW_SIZE = (640, 640)


def segment_intersects(pt1, pt2, xmin, xmax, threshold=1):
    values = [(pt1, True), (pt2, True), (xmin - threshold, False), (xmax + threshold, False)]
    values.sort()
    return values[0][1] == values[1][1]
