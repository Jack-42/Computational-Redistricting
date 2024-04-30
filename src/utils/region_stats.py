"""
@author Jack Ringer, Anthony Sharma
Date: 4/29/2024
Description:
Code for calculating statistics of regions.
"""


def get_original_pts(og_point_set, color_sets: dict, points_on_cuts=None):
    og_cset = og_point_set.get_sub_color_set(color_sets, use_og=True)
    if points_on_cuts is not None:
        og = og_cset.copy()
        og_cset = {}
        for color, cset in og.items():
            for p in cset:
                for p_prime in points_on_cuts:
                    if not (p.almost_equals(p_prime, decimal=2)):
                        og_cset[color] = og_cset.get(color, []) + [p]
    return og_cset


def get_majority_color(og_point_set, points_on_cuts, point_set, exclude_weights: bool):
    cset = point_set.color_sets
    if exclude_weights:
        cset = get_original_pts(og_point_set, cset, points_on_cuts)
    color_sizes = {k: len(cset[k]) for k in cset}

    first_majority = max(color_sizes, key=color_sizes.get)
    # check for tie
    first_size = color_sizes[first_majority]
    print(color_sizes)
    color_sizes[first_majority] = -1
    second_majority = max(color_sizes, key=color_sizes.get)
    if first_size == color_sizes[second_majority]:
        return -1  # no majority
    return first_majority


def get_region_majorities(
    og_point_set, points_on_cuts: list, point_sets: list, exclude_weights: bool
):
    # regions: list[ColorPointSet]
    majorities = list(
        map(
            lambda p_set: get_majority_color(
                og_point_set, points_on_cuts, p_set, exclude_weights
            ),
            point_sets,
        )
    )
    return majorities
