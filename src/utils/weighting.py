"""
@author Jack Ringer, Anthony Sharma
Date: 4/27/2024
Description:
Utilties for weighting points

The basic idea here is to give the minority color its share of representation (majority in n/(n+m)
regions), we ought to randomly highly weight points from the opposing color.

Note that we cannot determine which regions points will lie in ahead of time
(even if we first calculated the cuts, since the weighting will change the cut-line(s)).
"""

import numpy as np


def get_biased_weights_random(
    colors: np.ndarray, points_per_color: list[int], n_regions: int
):
    weights = np.ones(len(colors), dtype=int)
    minority_color = np.argmin(points_per_color)
    majority_color = np.argmax(points_per_color)
    if minority_color == majority_color:
        # no need to bias
        return weights
    # apply higher weighting to majority color points completely at random
    majority_indices = np.nonzero(colors == majority_color)[0]
    # want to isolate subset of majority points
    total_points = points_per_color[minority_color] + points_per_color[majority_color]
    n_points_to_choose = n_regions * points_per_color[minority_color] // total_points
    safety = (
        n_regions + 1
    )  # weighted points like to lie on the cut-lines - try to force some of them off
    n_points_to_choose = n_points_to_choose + safety
    n_points_to_choose = min(points_per_color[majority_color], n_points_to_choose)
    chosen_indices = np.random.choice(
        majority_indices, size=n_points_to_choose, replace=False
    )

    # isolate selected majority points
    # could make weight total_points to gurantee isolation as well, but given
    # our workaround implementation of weighted cuts want to avoid excess weight
    weights[chosen_indices] = points_per_color[majority_color]
    return weights
