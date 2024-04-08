"""
@author Jack Ringer, Anthony Sharma
Date: 4/7/2024
Description:
Algorithm for performing iterative ham-sandwich cuts
"""

import logging

from sympy import Line, Point, Polygon

from ham_sandwich import get_ham_sandwich_cut
from point_set import ColorPointSet
from utils.geometry import (
    get_points_inside,
    get_points_on_line,
    get_polygon,
    get_rectangular_region,
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
    # (for god knows what reason) - current_poly.vertices returns a tuple if current_poly a triangle
    new_points = list(current_poly.vertices) + [I1, I2]
    new_points = sort_points_ccw(new_points)
    # both new regions (polygons) will contain I1 and I2 - otherwise disjoint
    idx_1, idx_2 = new_points.index(I1), new_points.index(I2)
    if idx_1 > idx_2:
        tmp = idx_1
        idx_1 = idx_2
        idx_2 = tmp
    lower_points = new_points[0 : idx_1 + 1] + new_points[idx_2:]
    upper_points = new_points[idx_1 : idx_2 + 1]
    if len(lower_points) == 0 or len(upper_points) == 0:
        # ran out of points to cut
        return None, None
    lower_poly = get_polygon(lower_points)
    upper_poly = get_polygon(upper_points)
    return lower_poly, upper_poly


def _get_new_point_sets(
    cut: Line, point_set: ColorPointSet, lower_poly: Polygon, upper_poly: Polygon
):
    lower_color_set = {}
    upper_color_set = {}
    for c in point_set.color_sets:
        c_points = point_set.color_sets[c]
        c_points_in_lower = get_points_inside(c_points, lower_poly)
        c_points_in_upper = get_points_inside(c_points, upper_poly)
        n_lower, n_upper = len(c_points_in_lower), len(c_points_in_upper)

        c_points_on_cut = get_points_on_line(c_points, cut)

        # sanity-checks:
        # with current implementation, 1 point from each color should be on line
        # (with general position assumption and that the num. points for each color is odd)
        assert len(c_points_on_cut) == 1
        assert n_lower == n_upper
        assert n_lower + n_upper + 1 == len(c_points)

        # add point from cut if needed to maintain odd # of points for each color
        # TODO: causes issue later down the line when checking if point in polygon, need to fix
        # (maybe adjust by small epsilon?)
        if n_lower % 2 == 0:
            c_points_in_lower.append(c_points_on_cut[0])
            c_points_in_upper.append(c_points_on_cut[0])

        lower_color_set[c] = c_points_in_lower
        upper_color_set[c] = c_points_in_upper

    # TODO: this is pretty ugly, should clean up
    new_p_s_lower = ColorPointSet(
        None, None, None, color_sets=lower_color_set, defining_poly=lower_poly
    )
    new_p_s_upper = ColorPointSet(
        None, None, None, color_sets=upper_color_set, defining_poly=upper_poly
    )
    return new_p_s_lower, new_p_s_upper


def get_iterative_hs_cuts(
    point_set: ColorPointSet, k: int
) -> tuple[list[Line], list[Line]]:
    """
    Perform k-rounds of ham-sandich cuts
    """
    point_sets = [point_set]
    # rectangle bounding initial region
    domain = get_rectangular_region(
        point_set.lower_x, point_set.upper_x, point_set.lower_y, point_set.upper_y
    )
    point_set_polygons = [domain]
    cut_lines = []
    cut_segments = {}  # for visualization purposes
    for i in range(k):
        cut_segments[i] = []
        next_point_sets = []
        next_point_set_polygons = []
        for p_s, poly in zip(point_sets, point_set_polygons):
            # get cut
            k_cuts = get_ham_sandwich_cut(p_s)
            if len(k_cuts) > 1:
                logging.warning(
                    f"Found {len(k_cuts)} cuts at iteration {i}, but will only use first cut!"
                )
            hs_line = k_cuts[0]
            I1, I2 = poly.intersection(hs_line)
            if i < (k - 1):
                # calculate new intersections and regions created by cut
                lower_poly, upper_poly = _get_new_polygons(poly, I1, I2)
                if lower_poly is None:
                    # ran out of points
                    logging.warning(
                        f"Ran out of points at iteration {i}, you need to give more points with {k} cuts..."
                    )
                    i = k + 1
                else:
                    next_point_set_polygons.append(lower_poly)
                    next_point_set_polygons.append(upper_poly)

                    # use polygons to determine next point sets
                    new_p_s_lower, new_p_s_upper = _get_new_point_sets(
                        hs_line, p_s, lower_poly, upper_poly
                    )
                    next_point_sets.append(new_p_s_lower)
                    next_point_sets.append(new_p_s_upper)

            cut_lines.append(hs_line)
            # TODO: sometimes I1, I2 don't make sense (e.g., values outside original x/y bounds)
            cut_segments[i].append(Line(I1, I2))
        point_sets = next_point_sets
        point_set_polygons = next_point_set_polygons
    return cut_lines, cut_segments
