"""
@author Jack Ringer, Anthony Sharma
Date: 4/2/2024
Description: Generic utilities
"""

from functools import cmp_to_key

import numpy as np
from sympy import Line, Point, Polygon


def get_intersection(l1: Line, l2: Line):
    # sympy has weird syntax for this
    if l1.slope == l2.slope:
        return None
    intersections = l1.intersection(l2)
    if isinstance(intersections, list):
        return intersections[0]
    return intersections.args[0]


def get_polygon(ps: list[Point], already_sorted: bool = False) -> Polygon:
    """
    Get the polygon formed by a list of points
    """
    # when forming a Polygon with sympy points must be ordered
    sorted_ps = ps
    if not (already_sorted):
        sorted_ps = sort_points_ccw(ps)
    poly = Polygon(*sorted_ps)
    return poly


def get_points_inside(ps: list[Point], poly: Polygon) -> list[Point]:
    """
    Get the subset of ps which are inside poly
    """
    return [p for p in ps if poly.encloses_point(p)]


def get_rectangular_region(
    lower_x: float, upper_x: float, lower_y: float, upper_y: float
) -> Polygon:
    """
    Get the rectangular region defined by the given lower and upper bounds.
    """
    # points must be in ccw order
    points = [
        Point(lower_x, lower_y),
        Point(upper_x, lower_y),
        Point(upper_x, upper_y),
        Point(lower_x, upper_y),
    ]
    poly = get_polygon(points, already_sorted=True)
    return poly


def get_points_on_line(ps: list[Point], line: Line) -> list[Point]:
    """
    Get the subset of points on the given line
    """
    return [p for p in ps if line.contains(p)]


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
