"""
@author Jack Ringer, Anthony Sharma
Date: 4/2/2024
Description: Generic utilities
"""

from functools import cmp_to_key

import numpy as np
from sympy import Line, Point


def get_intersection(l1: Line, l2: Line):
    # sympy has weird syntax for this
    return l1.intersection(l2).args[0]


def xy_to_points(x: np.ndarray, y: np.ndarray) -> list[Point]:
    return list(map(lambda coords: Point(*coords), zip(x, y)))


def clockwise_compare(p1: Point, p2: Point, center: Point) -> int:
    # will return -1 if p1 should come before p2, 1 if p2 after p1, 0 if no preferance
    # this function based on: https://stackoverflow.com/p1/6989383
    if p1 == p2:
        return 0
    if (p1.x - center.x) >= 0 and (p2.x - center.x < 0):
        return 1
    if (p1.x - center.x) < 0 and (p2.x - center.x >= 0):
        return -1
    if (p1.x - center.x) == 0 and (p2.x - center.x) == 0:
        if (p1.y - center.y) >= 0 or (p2.y - center.y) >= 0:
            return p1.y > p2.y
        return p2.y > p1.y

    # compute the cross product of vectors (center -> p1) x (center -> p2)
    det = (p1.x - center.x) * (p2.y - center.y) - (p2.x - center.x) * (p1.y - center.y)
    if det < 0:
        return 1
    if det > 0:
        return -1

    # points p1 and p2 are on the same line from the center
    # check which point is closer to the center
    d1 = (p1.x - center.x) * (p1.x - center.x) + (p1.y - center.y) * (p1.y - center.y)
    d2 = (p2.x - center.x) * (p2.x - center.x) + (p2.y - center.y) * (p2.y - center.y)
    result = 1 if d1 > d2 else -1
    return result


def sort_points_ccw(ps: list[Point]):
    # sort list of 2D points in counter-clockwise order
    n = len(ps)
    center = Point(sum(p.x for p in ps) / n, sum(p.y for p in ps) / n)
    sorted_ps = sorted(
        ps, key=cmp_to_key(lambda p1, p2: clockwise_compare(p1, p2, center))
    )
    return sorted_ps


if __name__ == "__main__":
    ps = [
        Point(-2, 1),
        Point(2, 3),
        Point(-1, -2),
        Point(4, 3),
        Point(5, 1),
        Point(4, -1),
    ]
    sorted_ps = sort_points_ccw(ps)
    print(sorted_ps)
