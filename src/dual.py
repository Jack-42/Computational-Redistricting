"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Entry-point for code
"""

import numpy as np
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
from sympy import Point, Line

def dual_to_line(p : Point):
    assert isinstance(p, Point), 'Points only!'
    return Line (Point(0,p.y), slope=p.x)

def dual_to_point(l : Line):
    assert isinstance(l, Line), 'Lines only!'
    y_axis = Line (Point(0, 0), Point(0, 1))
    y_intersect = l.intersection(y_axis)
    return Point (l.slope, y_intersect[0].y)

p1 = Point (3,4)

print(dual_to_point(dual_to_line(p1)))
    

