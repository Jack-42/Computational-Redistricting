"""
@author Jack Ringer, Anthony Sharma
Date: 4/7/2024
Description:
Algorithm for performing iterative ham-sandwich cuts
"""

import logging

from shapely import Point, Polygon

from ham_sandwich import get_ham_sandwich_cut
from point_set import ColorPointSet
from utils.geometry import (
    Line,
    get_line_poly_intersection,
    get_points_inside,
    get_points_on_line,
    get_polygon,
    get_rectangular_region,
    get_vertices,
    sort_points_ccw,
)


def _get_new_polygons(
    current_poly: Polygon, I1: Point, I2: Point
) -> tuple[Polygon, Polygon]:
    """
    Each cut will split the existing region (polygon) into two new regions.
    This function calculates those two regions, where I1 and I2 are the intersection between the cut
    and the current_poly.
    """
    # each cut creates 2 new regions
    new_points = get_vertices(current_poly) + [I1, I2]
    new_points = sort_points_ccw(new_points)
    # both new regions (polygons) will contain I1 and I2 - otherwise disjoint
    idx_1, idx_2 = new_points.index(I1), new_points.index(I2)
    if idx_1 > idx_2:
        tmp = idx_1
        idx_1 = idx_2
        idx_2 = tmp
    lower_points = new_points[0 : idx_1 + 1] + new_points[idx_2:]
    upper_points = new_points[idx_1 : idx_2 + 1]
    lower_poly = get_polygon(lower_points)
    upper_poly = get_polygon(upper_points)
    return lower_poly, upper_poly


def _get_new_point_sets(
    cut: Line,
    point_set: ColorPointSet,
    lower_poly: Polygon,
    upper_poly: Polygon,
    points_on_cuts: list,
):
    lower_color_set = {}
    upper_color_set = {}
    for c in point_set.color_sets:
        c_points = point_set.color_sets[c]
        c_points_on_cut = get_points_on_line(c_points, cut)
        c_points_in_lower = get_points_inside(c_points, lower_poly)
        c_points_in_upper = get_points_inside(c_points, upper_poly)

        n_cut = len(c_points_on_cut)
        if n_cut > 0 and c_points_on_cut[0] in c_points_in_lower:
            c_points_in_lower.remove(c_points_on_cut[0])
        if n_cut > 0 and c_points_on_cut[0] in c_points_in_upper:
            c_points_in_upper.remove(c_points_on_cut[0])

        n_lower, n_upper = (
            len(c_points_in_lower),
            len(c_points_in_upper),
        )
        # sanity-checks:
        assert n_cut + n_lower + n_upper == len(
            c_points
        ), f"color {c} | n_cut, n_lower, n_upper: {n_cut}, {n_lower}, {n_upper}"
        assert n_lower == n_upper, f"color {c} | n_lower, n_upper: {n_lower}, {n_upper}"
        if n_cut > 0:
            # for visualization purposes later
            points_on_cuts.extend(c_points_on_cut)

        lower_color_set[c] = c_points_in_lower
        upper_color_set[c] = c_points_in_upper

    new_p_s_lower = ColorPointSet(color_sets=lower_color_set, defining_poly=lower_poly)
    new_p_s_upper = ColorPointSet(color_sets=upper_color_set, defining_poly=upper_poly)
    return new_p_s_lower, new_p_s_upper


def _sanity_check_points(p_s: ColorPointSet, i: int, k: int):
    if len(p_s.color_sets[0]) == 0 or len(p_s.color_sets[0]) == 0:
        logging.warning(
            f"Ran out of points at iteration {i}, you need to give more points with {k} cuts..."
        )
        return False
    return True


def _sanity_check_kth_cut(k_cuts: list, p_s: ColorPointSet, i: int) -> bool:
    if len(k_cuts) > 1:
        logging.warning(
            f"Found {len(k_cuts)} cuts at iteration {i}, but will only use first cut!"
        )
    elif len(k_cuts) == 0:
        logging.warning(
            f"Could not find a cut at iteration {i} with points: {p_s.color_sets}"
        )
        return False
    return True


def get_iterative_hs_cuts(
    point_set: ColorPointSet, k: int
) -> tuple[list[Line], list[Line]]:
    """
    Perform k-rounds of ham-sandwich cuts
    """
    point_sets = [point_set]
    # rectangle bounding initial region
    domain = get_rectangular_region(
        point_set.lower_x, point_set.upper_x, point_set.lower_y, point_set.upper_y
    )
    point_set_polygons = [domain]
    # maps color to points placed on cut - just maintained here for visualization later
    points_on_cuts = []
    cut_lines = []
    cut_segments = {}  # for visualization purposes
    error_occurred = False
    for i in range(k):
        cut_segments[i] = []
        next_point_sets = []
        next_point_set_polygons = []
        for p_s, poly in zip(point_sets, point_set_polygons):
            if not (_sanity_check_points(p_s, i, k)):
                error_occurred = True
                i = i + 1
                break
            # get cut
            k_cuts = get_ham_sandwich_cut(p_s)
            if not (_sanity_check_kth_cut(k_cuts, p_s, i)):
                error_occurred = True
                i = i + 1
                break
            hs_line = k_cuts[0]
            I1, I2 = get_line_poly_intersection(hs_line, poly)
            if i < (k - 1):
                # calculate new intersections and regions created by cut
                lower_poly, upper_poly = _get_new_polygons(poly, I1, I2)
                next_point_set_polygons.append(lower_poly)
                next_point_set_polygons.append(upper_poly)

                # use polygons to determine next point sets
                new_p_s_lower, new_p_s_upper = _get_new_point_sets(
                    hs_line, p_s, lower_poly, upper_poly, points_on_cuts
                )
                next_point_sets.append(new_p_s_lower)
                next_point_sets.append(new_p_s_upper)
            else:
                # still get points that were on cut for visualization
                c1_on_cut = get_points_on_line(p_s.color_sets[0], hs_line)
                c2_on_cut = get_points_on_line(p_s.color_sets[1], hs_line)
                points_on_cuts.extend(c1_on_cut)
                points_on_cuts.extend(c2_on_cut)

            cut_lines.append(hs_line)
            cut_segments[i].append(Line(p1=I1, p2=I2))
        point_sets = next_point_sets
        point_set_polygons = next_point_set_polygons
    return cut_lines, cut_segments, points_on_cuts, error_occurred
