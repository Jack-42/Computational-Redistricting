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

    # 2) pruning mechanism


if __name__ == "__main__":
    from point_set import ColorPointSet

    np.random.seed(42)
    point_set = ColorPointSet(10, "uni_random", "random", 2)
    weighted_2d_hs(point_set, None)
