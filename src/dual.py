"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Entry-point for code
"""

from sympy import Line, Point


def dual_to_line(p: Point):
    assert isinstance(p, Point), "Points only!"
    return Line(Point(0, -p.y), slope=p.x)


def dual_to_point(l: Line):
    assert isinstance(l, Line), "Lines only!"
    y_axis = Line(Point(0, 0), Point(0, 1))
    y_intersect = l.intersection(y_axis)
    return Point(l.slope, -y_intersect[0].y)


def dual_to_lines(ps: list[Point]):
    return list(map(dual_to_line, ps))


def dual_to_points(ls: list[Line]):
    return list(map(dual_to_point, ls))


if __name__ == "__main__":
    p1 = Point(3, 4)
    print(dual_to_point(dual_to_line(p1)))
