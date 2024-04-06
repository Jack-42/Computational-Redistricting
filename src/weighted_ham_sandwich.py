"""
@author Jack Ringer, Anthony Sharma
Date: 4/1/2024
Description:
Implementation of ham-sandwhich algorithm, based on: https://link.springer.com/chapter/10.1007/11589440_5
"""

import itertools
from typing import Optional

import numpy as np
import sympy as sp
from sympy import Line, Point

from dual import dual_to_lines
from utils.constants import EPSILON
from utils.utils import get_intersection


def get_quadrant(l_i: Line, l_A: Line, l_B: Line) -> int:
    """
    Get the quadrant for a given line l_i. The possible quadrants are:
    (1 = +, +, 2 = +, -, 3 = -, -, 4 = -, +), depending on
    "whether the line l_i crosses l_A above or below C, and whether it crosses l_B above
    or below C". C=intersection between l_A and l_B.
    Note we don't want to use the x-axis for l_A or l_B as this will cause all lines to fall in
    quadrants 1 and 2 (C.y=0=p_A.y=p_B.y).
    """
    if l_i.slope == l_A.slope or l_i.slope == l_B.slope or l_A.slope == l_B.slope:
        return None
    assert abs(l_A.slope) > 0 and abs(l_B.slope) > 0
    # should always be only exactly 1 point since l_A and l_B are not parallel
    C = get_intersection(l_A, l_B)
    p_A = get_intersection(l_i, l_A)
    p_B = get_intersection(l_i, l_B)
    # >= covers more extreme edge cases
    if p_A.y >= C.y and p_B.y >= C.y:
        return 1
    elif p_A.y >= C.y and p_B.y < C.y:
        return 2
    elif p_A.y < C.y and p_B.y < C.y:
        return 3
    else:
        return 4


def get_alpha(lines: list[Line], l_A: Line, l_B: Line):
    """
    Return the smallest value alpha s.t. each quadrant has >= alpha lines
    """
    n = len(lines)
    quadrant_map = {1: 0, 2: 0, 3: 0, 4: 0}
    for l in lines:
        q = get_quadrant(l, l_A, l_B)
        if q is not None:
            quadrant_map[q] = quadrant_map[q] + 1
    alpha = min(quadrant_map.values()) / n
    return alpha


def find_median_level(x: float, lines: list[Line], y_line: Line):
    y_vals = [get_intersection(line, y_line) + (x * line.slope) for line in lines]
    y_vals.sort()
    med = np.floor((len(y_vals) + 1) / 2)
    return y_vals[med - 1]


def get_median_level(lines: list[Line]):
    # TODO: implement this method, median level of arrangement
    pass


def find_partition(lines: list[Line], weights: list[Line]):
    """
    Construct a (1/4)-partition of the set of lines
    """
    # may want to use Las Vegas algo as suggested in: https://www.researchgate.net/publication/2851033_Optimization_in_Arrangements
    n = len(lines)
    assert n > 1
    # deterministic version, not trivial to implement
    line_slopes = [l.slope for l in lines]
    mu = np.median(line_slopes)
    L1 = [l for l in lines if l.slope <= mu]
    L2 = [l for l in lines if l.slope > mu]
    med_L1, med_L2 = get_median_level(L1), get_median_level(L2)

    """
    # las vegas algo, but only can get > 1/8 with constant probability - need 1/4
    l_A, l_B = None, None
    i = 0
    while l_A is None and l_B is None and i < 10000:
        i += 1
        print(i)
        l = random.choice(lines)
        mu = l.slope
        L_smaller = [l for l in lines if l.slope < mu]
        L_larger = [l for l in lines if l.slope > mu]
        if len(L_smaller) < 1 or len(L_larger) < 1:
            continue
        l_small, l_large = random.choice(L_smaller), random.choice(L_larger)
        C = get_intersection(l_small, l_large)
        l_A_ = Line(C, slope=mu)
        l_B_ = Line(C, slope=sp.oo)  # sp.oo = infinity -> vertical line
        alpha = get_alpha(lines, l_A_, l_B_)
        if alpha >= 0.125:
            l_A = l_A_
            l_B = l_B_
    """
    C = get_intersection(med_L1, med_L2)
    # get lines incident to C with known slope
    l_A = Line(C, slope=mu)
    l_B = Line(C, slope=sp.oo)  # sp.oo = infinity -> vertical line
    return l_A, l_B


def weighted_2d_hs(
    point_set,
    weights: Optional[np.ndarray[np.float64]] = None,
):
    """
    Weighted ham-sandwhich algo in 2-dimensions.
    Will return a line s.t. the plane L+ contains half the  points of blue_pts and red_pts,
    L- the other half - accounting for weights of the points.
    """
    if point_set.n_colors != 2:
        raise NotImplementedError(
            f"Currently only support 2-color ham-sandwhich cuts, given {point_set.n_colors} colors"
        )
    if weights is None:
        weights = np.ones_like(point_set.colors, dtype=np.float64)
    assert len(weights) > 2

    color_sets = point_set.color_sets
    # add formal infintessimal to one point from each set
    # may need to adjust depending on sensitivity (need to gurantee cut L is incident to one red, one blue pt)
    W = weights.copy()
    for color in point_set.unique_colors:
        first_i = np.argmax(point_set.colors == color)
        W[first_i] += EPSILON

    # 1) convert points to their duals (lines)
    T = {
        c: dual_to_lines(c_set) for c, c_set in color_sets.items()
    }  # T[i] = set of lines for color i
    # 2) find (1/4)-partition
    T_U = list(itertools.chain(*T.values()))
    l_A, l_B = find_partition(T_U, weights)
    # 3) calculate parity
    # 4) pruning mechanism
    # 5) recurse


if __name__ == "__main__":
    from point_set import ColorPointSet

    np.random.seed(42)
    point_set = ColorPointSet(10, "uni_random", "random", 2)
    weighted_2d_hs(point_set, None)
