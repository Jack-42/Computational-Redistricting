"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Entry-point for code
"""

import argparse

import numpy as np

from constants import *
from point_set import ColorPointSet
from visualization import plot_points


def list_of_floats(arg):
    return list(map(float, arg.split(",")))


def parse_args():
    parser = argparse.ArgumentParser(
        prog="main",
        description="Visualize points with given params",
    )
    parser.add_argument(
        "--n_points",
        type=int,
        required=True,
        default=argparse.SUPPRESS,
        help="number of points",
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
    parser.add_argument(
        "--n_colors", type=int, default=2, help="number of colors to use"
    )
    parser.add_argument(
        "--color_probs",
        type=list_of_floats,
        default=None,
        help="probability of sampling each color",
    )
    parser.add_argument("--seed", type=int, default=42, help="random seed")
    parser.add_argument(
        "--fig_save_path",
        type=str,
        default=None,
        help="path to save figure to (optional)",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    np.random.seed(args.seed)
    point_set = ColorPointSet(
        args.n_points,
        args.sample_method,
        args.color_method,
        args.n_colors,
        args.color_probs,
    )
    plot_points(point_set, args.fig_save_path)
