"""
@author Jack Ringer, Anthony Sharma
Date: 5/4/2024
Description:
Code for evaluating how subsampling/weighting scheme impacts region majority outcomes.
This code is could be improved to be 'cleaner', but it gets the job done.
"""

import argparse
import logging
import os
import time

import numpy as np
import pandas as pd
from tqdm import tqdm

from iterative_ham import get_iterative_hs_cuts
from point_set import ColorPointSet, subsample
from utils.constants import *
from utils.geometry import get_points_near_cuts
from utils.region_stats import get_region_majorities


def _get_ppcs(total_points: int, ratios: list[float]):
    # points per color for different ratios between minority/majority
    ppcs = []
    for i in range(len(ratios)):
        c1_pts = int(np.floor(ratios[i] * total_points))
        c2_pts = total_points - c1_pts
        ppcs.append([c1_pts, c2_pts])
    return ppcs


def _get_majority_share(region_majorites: np.ndarray, majority_color: int):
    majority_count = len(np.where(region_majorites == majority_color)[0])
    return majority_count / len(region_majorites)


def _eval_run(
    k: int,
    points_per_color: tuple,
    seed: int,
    weight_method: str,
    subsample_points: bool,
    subsample_ratio: float,
):
    np.random.seed(seed)
    point_set = ColorPointSet(
        points_per_color=points_per_color,
        color_method=RANDOM,
        weighting_method=weight_method,
        k=k,
    )
    og_point_set = None
    if subsample_points:
        sub_point_set = subsample(point_set, subsample_ratio)
        # will swap back to original set for final eval
        og_point_set = point_set
        point_set = sub_point_set
    regions, cuts, _, points_on_cuts, err = get_iterative_hs_cuts(
        point_set, k, True, og_point_set
    )
    # if using weighted case, then consider all points close to a cut to be on the cut
    majority_color = np.argmax(points_per_color)
    if weight_method == WEIGHT_MAJORITY:
        cut_tol = 0.01  # NOTE: if there is a point within cut_tol of two cuts this will cause an error
        # gather together all points that were part of cut
        # NOTE: args.weight_method == BIASED_WEIGHT => only majority points are weighted
        points_near_cuts = get_points_near_cuts(
            point_set.color_sets[majority_color], cuts, cut_tol
        )
        points_on_cuts.extend(points_near_cuts)
        points_on_cuts = list(set(points_on_cuts))
    if not err:
        if subsample_points:
            point_set = og_point_set
        exclude_weights = weight_method == WEIGHT_MAJORITY
        majorities = get_region_majorities(
            point_set, points_on_cuts, regions, exclude_weights
        )
        return _get_majority_share(majorities, majority_color)
    else:
        return -1


def evaluate_params(
    k_vals: list[int],
    ppcs: list[list[int]],
    seeds: list[int],
    use_subsampling: bool,
    subsample_ratios: list[float],
    weight_method: str,
):
    if subsample_ratios is None:
        assert not (use_subsampling)
        subsample_ratios = [0.0]
    results_rows = []
    for seed in tqdm(seeds, desc="seed progress", unit="seed"):
        for ppc in ppcs:
            for k in k_vals:
                for sr in subsample_ratios:
                    t0 = time.time()
                    majority_share = _eval_run(
                        k, ppc, seed, weight_method, use_subsampling, sr
                    )
                    runtime = time.time() - t0  # in seconds
                    row = {
                        "k": k,
                        "points_per_color": ppc,
                        "seed": seed,
                        "weight_method": weight_method,
                        "use_subsampling": use_subsampling,
                        "subsample_ratio": sr,
                        "majority_share": majority_share,
                        "runtime": runtime,
                    }
                    results_rows.append(row)
    return results_rows


def weighted_main(
    save_path: str,
    k_vals: list[int],
    seeds: list[int],
    ppcs: list[list[int]],
):
    print("Running evaluation...")
    rows = evaluate_params(k_vals, ppcs, seeds, False, None, WEIGHT_MAJORITY)
    df = pd.DataFrame.from_dict(rows)
    df.to_csv(save_path)
    print("Saved results to:", save_path)


def subsample_main(
    save_path: str,
    k_vals: list[int],
    seeds: list[int],
    ppcs: list[list[int]],
):
    # subsampling
    subsample_ratios = [0.05, 0.1, 0.2, 0.4]

    print("Running evaluation...")
    rows = evaluate_params(k_vals, ppcs, seeds, True, subsample_ratios, WEIGHT_UNIFORM)
    df = pd.DataFrame.from_dict(rows)
    df.to_csv(save_path)
    print("Saved results to:", save_path)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="eval_main",
        description="Program to evaluate different methods",
    )
    parser.add_argument(
        "--method",
        type=str,
        required=True,
        help=f"method to evaluate, choose from: (weighted, subsampling)",
    )
    parser.add_argument(
        "--save_path",
        type=str,
        required=True,
        help="path to save results file to. should end with .csv",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    assert args.save_path.endswith(
        ".csv"
    ), f"save_path must end with .csv, given:{args.save_path}"

    # make sure save dir exists
    save_dir = os.path.dirname(args.save_path)
    if len(save_dir) > 0:
        os.makedirs(save_dir, exist_ok=True)

    # shared params
    logging.basicConfig(level=logging.CRITICAL)
    total_points = 500
    k_vals = [2, 3, 4]
    seeds = np.arange(0, 10, dtype="int")
    ratios = [1 / 4, 1 / 3, 2 / 5]
    ppcs = _get_ppcs(total_points, ratios)

    if args.method.lower() == "weighted":
        weighted_main(args.save_path, k_vals, seeds, ppcs)
    elif args.method.lower() == "subsampling":
        subsample_main(args.save_path, k_vals, seeds, ppcs)
    else:
        raise ValueError(f"Unrecognized method: {args.method}")
