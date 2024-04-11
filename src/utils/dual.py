"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Duality transforms
"""

from shapely import Point

from utils.geometry import Line


# transforms described in: https://link.springer.com/chapter/10.1007/11589440_5
def dual_to_line(p: Point):
    return Line(p1=Point(0, p.y), slope=p.x)


def dual_to_point(l: Line) -> Point:
    y_axis = Line(Point(0, 0), Point(0, 1))
    y_intersect = l.intersection(y_axis)
    return Point(-l.slope, y_intersect[0].y)


def dual_to_lines(ps: list[Point]):
    return list(map(dual_to_line, ps))


def dual_to_points(ls: list[Line]):
    return list(map(dual_to_point, ls))


# transforms for unweighted ham-sandwich
def uw_dual_to_line(p: Point):
    return Line(p1=Point(0, -p.y), slope=p.x)


def uw_dual_to_lines(ps: list[Point]):
    return list(map(uw_dual_to_line, ps))
