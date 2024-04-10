"""
@author Jack Ringer, Anthony Sharma
Date: 4/6/2024
Description:
Implementation of (unweighted) ham-sandwich algo in 2D.
Based on the implementation here: https://github.com/anjali411/Ham-Sandwich-Cut/blob/master/hamSandwichCut.py
"""

import numpy as np
from shapely import LineString, Point

from point_set import ColorPointSet
from utils.dual import uw_dual_to_lines
from utils.geometry import Line, get_line_intersection


def get_line_y_intercepts(lines: list[Line]):
    line_yints = [l.y_int for l in lines]
    return line_yints


def find_median_level(x: float, lines: list[Line]):
    y_vals = [line.y_int + (x * line.slope) for line in lines]
    y_vals.sort()
    med = (len(y_vals) + 1) // 2
    return y_vals[med - 1]


def odd_intersection(interval, c1_duals, c2_duals):
    left = interval[0]
    right = interval[1]

    lm_c1 = find_median_level(left, c1_duals)
    lm_c2 = find_median_level(left, c2_duals)

    rm_c1 = find_median_level(right, c1_duals)
    rm_c2 = find_median_level(right, c2_duals)

    v1 = lm_c1 - lm_c2
    v2 = rm_c1 - rm_c2
    # cross product - if negative then v1 and v2 point in opposite directions
    return v1 * v2 < 0


def get_intersections(interval, duals):
    intersections = []
    for i in range(len(duals)):
        for j in range(len(duals)):
            if i < j:
                intersection_ = get_line_intersection(duals[i], duals[j])
                if intersection_.x == np.inf:
                    pass
                elif interval[0] < intersection_.x and interval[1] > intersection_.x:
                    intersections.append(intersection_)
                else:
                    pass

    intersections.sort(key=lambda I: I.x)
    return intersections


def get_med_linestring(interval, duals, intersections):
    med_levels = [Point(interval[0], find_median_level(interval[0], duals))]
    med_levels.extend(
        [Point(inter.x, find_median_level(inter.x, duals)) for inter in intersections]
    )
    med_levels.extend([Point(interval[1], find_median_level(interval[1], duals))])
    return LineString(med_levels)


def median_intersection(interval, c1_duals, c2_duals):
    c1_intersections = get_intersections(interval, c1_duals)
    c2_intersections = get_intersections(interval, c2_duals)

    c1_med_linestring = get_med_linestring(interval, c1_duals, c1_intersections)
    c2_med_linestring = get_med_linestring(
        interval,
        c2_duals,
        c2_intersections,
    )

    ham_cut_points = c1_med_linestring.intersection(c2_med_linestring)
    if isinstance(ham_cut_points, Point):
        ham_cut_points = [ham_cut_points]
    ham_cut_dual = uw_dual_to_lines(ham_cut_points)
    return ham_cut_dual


def get_ham_sandwich_cut(point_set: ColorPointSet):
    if point_set.n_colors != 2:
        raise ValueError("Ham-sandwich cuts in 2D only can support 2 colors!")
    min_interval_size = 1
    c1_points = point_set.color_sets[0]
    c2_points = point_set.color_sets[1]
    assert len(c1_points) % 2 == 1, "Number of points for color 1 must be odd!"
    assert len(c2_points) % 2 == 1, "Number of points for color 2 must be odd!"

    # get duals and y-intercepts of dual lines
    c1_duals = uw_dual_to_lines(c1_points)
    c2_duals = uw_dual_to_lines(c2_points)

    # get initial interval for binary search
    # ival arbitrary here, just want large interval relative to lower_x and higher_x
    i = max(abs(point_set.lower_x), abs(point_set.upper_x))
    ival = (i + 10) ** 2
    interval = (point_set.lower_x - ival, point_set.upper_x + ival)
    # binary search
    while (interval[1] - interval[0]) > min_interval_size:
        mid = float((interval[0] + interval[1]) / 2.0)
        left_int = [interval[0], mid]
        right_int = [mid, interval[1]]
        if odd_intersection(left_int, c1_duals, c2_duals):
            interval = left_int
        else:
            interval = right_int
    ham_cuts = median_intersection(interval, c1_duals, c2_duals)
    return ham_cuts
