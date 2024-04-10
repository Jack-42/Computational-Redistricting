"""
@author Jack Ringer, Anthony Sharma
Date: 4/2/2024
Description: Generic utilities
"""

from functools import cmp_to_key
from typing import Union

import numpy as np
from shapely import LineString, Point, Polygon, intersection


class Line:
    def __init__(
        self,
        p1: Point = None,
        p2: Point = None,
        slope: float = None,
        y_int: float = None,
        domain_lower_x: float = -1,
        domain_upper_x: float = 1,
    ) -> None:
        self.p1 = None
        self.p2 = None
        self.slope = None
        self.y_int = None
        if slope is not None and y_int is not None:
            self.slope = slope
            self.y_int = y_int
        elif slope is not None and p1 is not None:
            self.slope = slope
            self.p1 = p1
        elif p1 is not None and p2 is not None:
            assert p1.x != p2.x
            self.p1 = p1
            self.p2 = p2
        elif slope is not None and p1 is not None and p2 is None:
            self.p1 = p1
            self.slope = slope
        else:
            raise ValueError("Invalid combination of arguments provided.")
        if self.p1 is None:
            self.p1 = Point(0, self.y_int)
        if self.y_int is None:
            self.y_int = self.p1.y - self.slope * self.p1.x
        if self.p2 is None:
            p2_x = self.p1.x + 1
            p2_y = self.slope * p2_x + self.y_int
            self.p2 = Point(p2_x, p2_y)
        if self.slope is None:
            self.slope = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
        lower_y = self.slope * domain_lower_x + self.y_int
        upper_y = self.slope * domain_upper_x + self.y_int
        self.lstring = LineString(
            [(domain_lower_x, lower_y), (domain_upper_x, upper_y)]
        )


def get_line_intersection(l1: Line, l2: Line) -> Union[None, Point]:
    if np.isclose(l1.slope, l2.slope):
        # limitations of floating-point precision could cause incorrect results in extreme cases,
        # but not a problem practically-speaking
        return None
    x = (l2.y_int - l1.y_int) / (l1.slope - l2.slope)
    y = l1.slope * x + l1.y_int
    return Point(x, y)


def get_line_poly_intersection(l: Line, poly: Polygon):
    coords = intersection(poly, l.lstring).coords
    return list(map(Point, coords))


def get_polygon(ps: list[Point], already_sorted: bool = False) -> Polygon:
    """
    Get the polygon formed by a list of points
    """
    # when forming a Polygon points must be ordered
    sorted_ps = ps
    if not (already_sorted):
        sorted_ps = sort_points_ccw(ps)
    poly = Polygon(sorted_ps)
    return poly


def get_vertices(poly: Polygon) -> list[Point]:
    # shapely includes initial point at both ends of the list
    tup_coords = list(poly.exterior.coords)[:-1]
    return list(map(Point, tup_coords))


def get_points_inside(ps: list[Point], poly: Polygon) -> list[Point]:
    """
    Get the subset of ps which are inside poly
    """
    return [p for p in ps if poly.contains(p)]


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


def _on_line(p: Point, line: Line):
    return np.isclose((p.x * line.slope + line.y_int), p.y)


def get_points_on_line(ps: list[Point], line: Line) -> list[Point]:
    """
    Get the subset of points on the given line
    """
    return [p for p in ps if _on_line(p, line)]


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
