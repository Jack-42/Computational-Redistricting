"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Entry-point for code
"""

import argparse

import numpy as np

from ham_sandwich import get_ham_sandwich_cut
from iterative_ham import get_iterative_hs_cuts
from point_set import ColorPointSet
from utils.constants import *
from visualization import plot_lines, plot_point_set


def list_of_int(arg):
    return list(map(int, arg.split(",")))


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
        help="method for sampling spatial points",
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
        "--k",
        type=int,
        default=1,
        help="number of iterations to perform with iterative ham-sandwich algorithm",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    np.random.seed(args.seed)
    point_set = ColorPointSet(
        args.points_per_color,
        args.sample_method,
        args.color_method,
    )
    if args.algorithm == HAM_SANDWICH:
        cuts = get_ham_sandwich_cut(point_set)
        plot_point_set(point_set, show=False)
        plot_lines(cuts, save_path=args.fig_save_path)
    elif args.algorithm == ITERATIVE_HAM_SANDWICH:
        cuts, cut_segments = get_iterative_hs_cuts(point_set, args.k)
        plot_point_set(point_set, show=False)
        plot_lines(cuts, save_path=args.fig_save_path, segments_only=True)
    else:
        raise NotImplementedError(f"Given algorithm not implemented: {args.algorithm}")
