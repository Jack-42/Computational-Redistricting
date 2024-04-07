"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Duality transforms
"""

from typing import Union

from shapely import Point as ShapelyPoint
from sympy import Line, Point


# transforms described in: https://link.springer.com/chapter/10.1007/11589440_5
def dual_to_line(p: Union[Point, ShapelyPoint]):
    return Line(Point(0, p.y), slope=p.x)


def dual_to_point(l: Line):
    y_axis = Line(Point(0, 0), Point(0, 1))
    y_intersect = l.intersection(y_axis)
    return Point(-l.slope, y_intersect[0].y)


def dual_to_lines(ps: list[Point]):
    return list(map(dual_to_line, ps))


def dual_to_points(ls: list[Line]):
    return list(map(dual_to_point, ls))


# transforms for unweighted ham-sandwich
def uw_dual_to_line(p: Union[Point, ShapelyPoint]):
    return Line(Point(0, -p.y), slope=p.x)


def uw_dual_to_lines(ps: list[Point]):
    return list(map(dual_to_line, ps))


if __name__ == "__main__":
    p1 = Point(3, 4)
    l1 = dual_to_line(p1)
    print(p1, l1)
    print(dual_to_point(dual_to_line(p1)))
