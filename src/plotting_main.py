"""
@author Jack Ringer, Anthony Sharma
Description:
File for plotting results from eval_main.py
"""

import argparse
import ast
import os
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ci == confidence interval
def plot_xy_ci(
    x: np.ndarray,
    y: np.ndarray,
    ci: np.ndarray,
    xlabel: str,
    ylabel: str,
    save_path: str,
    ideal_y: Optional[np.ndarray] = None,
    ideal_y_label: Optional[str] = None,
):
    fig, ax = plt.subplots()
    ax.plot(x, y, marker="o", label=ylabel)
    ax.fill_between(x, (y - ci), (y + ci), color="b", alpha=0.1, label="95% CI")
    if ideal_y is not None:
        ax.plot(x, ideal_y, marker="x", color="r", label=ideal_y_label)
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_xticks(np.unique(x))
    plt.savefig(save_path, dpi=300)
    plt.close()


def plot_grouping(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    save_path: str,
    ideal_y_col: Optional[str] = None,
    n_seeds: int = 10,
):
    df_mean = df[[x_col, y_col]].groupby(x_col).mean()
    df_std = df[[x_col, y_col]].groupby(x_col).std()
    x, y = (
        df_mean.index,
        df_mean[y_col],
    )
    ci = 1.96 * df_std[y_col] / np.sqrt(n_seeds)

    ideal_y = None
    if ideal_y_col is not None:
        df_ideal = df[[x_col, ideal_y_col]].groupby(x_col).mean()
        ideal_y = df_ideal[ideal_y_col]
    plot_xy_ci(x, y, ci, x_col, y_col, save_path, ideal_y, ideal_y_col)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="plotting_main",
        description="Script to plot eval metrics",
    )
    parser.add_argument(
        "--csv_path",
        type=str,
        required=True,
        help=f"path to results csv file",
    )
    parser.add_argument(
        "--save_dir",
        type=str,
        required=True,
        help="directory to save figures to",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    df = pd.read_csv(args.csv_path, converters={"points_per_color": ast.literal_eval})
    ideal_majority_share_col = r"$\delta$"
    majority_share_col = "majorityShare"
    majority_share_dist_from_ideal_col = r"$\mu$"
    df.rename({"majority_share": majority_share_col}, inplace=True, axis=1)
    # renaming to match report
    color_ratio = r"$\rho$"
    df[color_ratio] = df["points_per_color"].map(
        lambda ppc: ppc[0] / (ppc[0] + ppc[1])
    )  # ppc[0] assumed to be minority color
    df[majority_share_dist_from_ideal_col] = df[majority_share_col] - (
        1 - df[color_ratio]
    )
    df[ideal_majority_share_col] = 1 - df[color_ratio]
    os.makedirs(args.save_dir, exist_ok=True)
    plot_grouping(
        df,
        color_ratio,
        majority_share_col,
        os.path.join(args.save_dir, "color_ratio.png"),
        ideal_majority_share_col,
    )
    plot_grouping(
        df,
        color_ratio,
        majority_share_dist_from_ideal_col,
        os.path.join(args.save_dir, "color_ratio_dist.png"),
    )
    plot_grouping(
        df,
        "k",
        majority_share_dist_from_ideal_col,
        os.path.join(args.save_dir, "k.png"),
    )

    sub_df = df[df["use_subsampling"]]
    if len(sub_df) > 0:
        plot_grouping(
            df,
            "subsample_ratio",
            majority_share_dist_from_ideal_col,
            os.path.join(args.save_dir, "sub_ratio.png"),
        )
