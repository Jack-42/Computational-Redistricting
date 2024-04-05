"""
@author Jack Ringer, Anthony Sharma
Date: 4/1/2024
Description:
Implementation of ham-sandwhich algorithm, based on: https://link.springer.com/chapter/10.1007/11589440_5
"""

from typing import Optional

import numpy as np
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
    assert l_A.slope != l_B.slope, "l_A and l_B cannot be parallel!"
    assert abs(l_A.slope) > 0 and abs(l_B.slope) > 0
    # should always be only exactly 1 point since l_A and l_B are not parallel
    C = get_intersection(l_A, l_B)
    p_A = get_intersection(l_i, l_A)
    p_B = get_intersection(l_i, l_B)
    # >= covers more extreme edge cases
    if p_A.y >= C.y and p_B >= C.y:
        return 1
    elif p_A.y >= C.y and p_B < C.y:
        return 2
    elif p_A.y < C.y and p_B < C.y:
        return 3
    else:
        return 4


def find_partition(lines: list[Line]):
    """
    Construct a (1/4)-partition of the set of lines
    """
    # may want to use Las Vegas algo as suggested in: https://www.researchgate.net/publication/2851033_Optimization_in_Arrangements
    pass


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
    # 3) calculate parity
    # 4) pruning mechanism
    # 5) recurse


if __name__ == "__main__":
    from point_set import ColorPointSet

    np.random.seed(42)
    point_set = ColorPointSet(10, "uni_random", "random", 2)
    weighted_2d_hs(point_set, None)
