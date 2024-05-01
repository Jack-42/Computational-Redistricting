"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Entry-point for code
"""

import argparse
import logging
import logging.config

import numpy as np

from ham_sandwich import get_ham_sandwich_cut
from iterative_ham import get_iterative_hs_cuts
from point_set import ColorPointSet
from utils.constants import *
from utils.geometry import get_points_near_cuts
from utils.region_stats import get_region_majorities
from visualization import plot_k_cuts, plot_lines, plot_point_set


def list_of_int(arg):
    return list(map(int, arg.split(",")))


def list_of_float(arg):
    return list(map(float, arg.split(",")))


def parse_args():
    parser = argparse.ArgumentParser(
        prog="main",
        description="Visualize points/lines with given params",
    )
    parser.add_argument(
        "--points_per_color",
        required=True,
        type=list_of_int,
        default=argparse.SUPPRESS,
        help="number of points to use for each color",
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        default=HAM_SANDWICH,
        help="algorithm to visualize",
    )
    parser.add_argument(
        "--sample_method",
        type=str,
        default=UNIFORM_RANDOM,
        help=f"method for sampling spatial points, choose from: {UNIFORM_RANDOM}",
    )
    parser.add_argument(
        "--weight_method",
        type=str,
        default=UNIFORM_WEIGHT,
        help=f"how to weight points, choose from: {UNIFORM_WEIGHT, BIASED_WEIGHT}",
    )
    parser.add_argument(
        "--color_method",
        type=str,
        default=RANDOM,
        help="method for sampling color points",
    )
    parser.add_argument("--seed", type=int, default=42, help="random seed")
    parser.add_argument(
        "--fig_save_path",
        type=str,
        default=None,
        help="path to save figure to (optional)",
    )
    parser.add_argument(
        "--show_fig",
        action="store_true",
        help="show figure if set",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=1,
        help=f"({ITERATIVE_HAM_SANDWICH} only) number of iterations to perform",
    )
    parser.add_argument(
        "--calculate_final_regions",
        action="store_true",
        help=f"({ITERATIVE_HAM_SANDWICH} only) calculate final regions formed by cuts and log their statistics",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    np.random.seed(args.seed)
    point_set = ColorPointSet(
        points_per_color=args.points_per_color,
        spatial_method=args.sample_method,
        color_method=args.color_method,
        weighting_method=args.weight_method,
        k=args.k,
    )
    if args.algorithm == HAM_SANDWICH:
        cuts = get_ham_sandwich_cut(point_set)
        plot_point_set(point_set, show=False, plot_bbox=True, hide_ticks=True)
        plot_lines(cuts, save_path=args.fig_save_path, show=args.show_fig)
    elif args.algorithm == ITERATIVE_HAM_SANDWICH:
        regions, cuts, cut_segments, points_on_cuts, err = get_iterative_hs_cuts(
            point_set, args.k, args.calculate_final_regions
        )
        # if using weighted case, then consider all points close to a cut to be on the cut
        cut_tol = 0.01  # NOTE: if there is a point within cut_tol of two cuts this will cause an error
        if args.weight_method == BIASED_WEIGHT:
            # gather together all points that were part of cut
            # NOTE: args.weight_method == BIASED_WEIGHT => only majority points are weighted
            majority_i = np.argmax(args.points_per_color)
            points_near_cuts = get_points_near_cuts(
                point_set.color_sets[majority_i], cuts, cut_tol
            )
            points_on_cuts.extend(points_near_cuts)
            points_on_cuts = list(set(points_on_cuts))
        if not err:
            if args.calculate_final_regions:
                exclude_weights = args.weight_method == BIASED_WEIGHT
                majorities = get_region_majorities(
                    point_set, points_on_cuts, regions, exclude_weights
                )
                print(f"Region majorities: {majorities}")
            # special_indices = points that were intersected by a cut
            # used to make these points less opaque for visualization purposes
            intersected_points = point_set.get_matching_indices(points_on_cuts)
            plot_point_set(
                point_set,
                show=False,
                special_indices=intersected_points,
                plot_bbox=True,
                hide_ticks=True,
                hide_weighted_pts=True,
            )
            plot_k_cuts(
                cut_segments,
                args.k,
                save_path=args.fig_save_path,
                segments_only=True,
                show=args.show_fig,
            )
        else:
            logging.error(
                "An error occured, please check the message above and/or your input points"
            )
    elif args.algorithm == VISUALIZE_POINTS:
        plot_point_set(point_set, save_path=args.fig_save_path)
    # elif args.algorithm == VORONOI_SAMPLING:
    # (sampled_points, voronoi) = get_voronoi_sample(point_set)
    # plot_point_set(sampled_points, show=False)
    # plot_lines(voronoi, save_path=args.fig_save_path, show=args.show_fig)

    else:
        raise NotImplementedError(f"Given algorithm not implemented: {args.algorithm}")
