"""
@author Jack Ringer, Anthony Sharma
Date: 4/29/2024
Description:
Code for calculating statistics of regions.
"""


def get_sub_color_set(cset: dict, cset_query: dict, exclude_pts: list):
    final_set = {}
    for color in cset.keys():
        sub_cset = cset[color]
        sub_query_cset = cset_query[color]
        for p in sub_query_cset:
            if any(
                p.equals_exact(p_prime, tolerance=1e-8) for p_prime in sub_cset
            ) and not (
                any(p.equals_exact(p_prime, tolerance=1e-8) for p_prime in exclude_pts)
            ):
                final_set[color] = final_set.get(color, []) + [p]
    return final_set


def get_original_pts(og_point_set, color_sets: dict, points_on_cuts=None):
    if points_on_cuts is None:
        points_on_cuts = []
    og_cset = get_sub_color_set(og_point_set.og_color_sets, color_sets, points_on_cuts)
    return og_cset


def get_majority_color(og_point_set, points_on_cuts, point_set, exclude_weights: bool):
    cset = point_set.color_sets
    if exclude_weights:
        cset = get_original_pts(og_point_set, cset, points_on_cuts)
    color_sizes = {k: len(cset[k]) for k in cset}
    first_majority = max(color_sizes, key=color_sizes.get)
    # check for tie
    first_size = color_sizes[first_majority]
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
