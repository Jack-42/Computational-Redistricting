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
from point_set import ColorPointSet, subsample
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
        "--program",
        type=str,
        default=HAM_SANDWICH,
        help=f"program to visualize, choose from: {HAM_SANDWICH, ITERATIVE_HAM_SANDWICH, VISUALIZE_POINTS}",
    )
    parser.add_argument(
        "--weight_method",
        type=str,
        default=WEIGHT_UNIFORM,
        help=f"how to weight points, choose from: {WEIGHT_UNIFORM, WEIGHT_MAJORITY}",
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
    parser.add_argument(
        "--subsample_points",
        action="store_true",
        help="subsample the original set of points before performing HSC",
    )
    parser.add_argument(
        "--subsample_ratio",
        type=float,
        default=0.1,
        help="ratio of points to sample, will sample floor(n_points * ratio) total points",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    np.random.seed(args.seed)
    point_set = ColorPointSet(
        points_per_color=args.points_per_color,
        color_method=args.color_method,
        weighting_method=args.weight_method,
        k=args.k,
    )
    og_point_set = None
    if args.subsample_points:
        sub_point_set = subsample(point_set, args.subsample_ratio)
        # will swap back to original set for visualization
        og_point_set = point_set
        point_set = sub_point_set
    if args.program == HAM_SANDWICH:
        cuts = get_ham_sandwich_cut(point_set)
        if args.subsample_points:
            point_set = og_point_set
        plot_point_set(point_set, show=False, plot_bbox=True, hide_ticks=True)
        plot_lines(cuts, save_path=args.fig_save_path, show=args.show_fig)
    elif args.program == ITERATIVE_HAM_SANDWICH:
        regions, cuts, cut_segments, points_on_cuts, err = get_iterative_hs_cuts(
            point_set, args.k, args.calculate_final_regions, og_point_set
        )
        # if using weighted case, then consider all points close to a cut to be on the cut
        cut_tol = 0.01  # NOTE: if there is a point within cut_tol of two cuts this will cause an error
        if args.weight_method == WEIGHT_MAJORITY:
            # gather together all points that were part of cut
            # NOTE: args.weight_method == BIASED_WEIGHT => only majority points are weighted
            majority_i = np.argmax(args.points_per_color)
            points_near_cuts = get_points_near_cuts(
                point_set.color_sets[majority_i], cuts, cut_tol
            )
            points_on_cuts.extend(points_near_cuts)
            points_on_cuts = list(set(points_on_cuts))
        if not err:
            if args.subsample_points:
                point_set = og_point_set
            if args.calculate_final_regions:
                exclude_weights = args.weight_method == WEIGHT_MAJORITY
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
    elif args.program == VISUALIZE_POINTS:
        plot_point_set(point_set, save_path=args.fig_save_path)
    # elif args.program == VORONOI_SAMPLING:
    # (sampled_points, voronoi) = get_voronoi_sample(point_set)
    # plot_point_set(sampled_points, show=False)
    # plot_lines(voronoi, save_path=args.fig_save_path, show=args.show_fig)

    else:
        raise NotImplementedError(f"Given program not implemented: {args.program}")
