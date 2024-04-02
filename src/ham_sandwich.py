"""
@author Jack Ringer, Anthony Sharma
Date: 4/1/2024
Description:
Implementation of ham-sandwhich algorithm, based on: https://link.springer.com/chapter/10.1007/11589440_5
"""

from typing import Optional

import numpy as np
from sympy import Line, Point


def weighted_2d_hs(
    point_set,
    weights: Optional[np.ndarray],
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

    # convert points to their duals (lines)
    T = []  # T[i] = set of lines for color i
    color_sets = point_set.color_sets


if __name__ == "__main__":
    from point_set import ColorPointSet

    np.random.seed(42)
    point_set = ColorPointSet(10, "uni_random", "random", 2)
    weighted_2d_hs(point_set, None)
