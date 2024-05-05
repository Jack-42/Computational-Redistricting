"""
@author Jack Ringer, Anthony Sharma
Description:
File for plotting results from eval_main.py
"""

import argparse
import ast
import os

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
):
    fig, ax = plt.subplots()
    ax.plot(x, y, marker="o")
    ax.fill_between(x, (y - ci), (y + ci), color="b", alpha=0.1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(np.unique(x))
    plt.savefig(save_path, dpi=300)
    plt.close()


def plot_grouping(
    df: pd.DataFrame, x_col: str, y_col: str, save_path: str, n_seeds: int = 10
):
    df_mean = df[[x_col, y_col]].groupby(x_col).mean()
    df_std = df[[x_col, y_col]].groupby(x_col).std()
    df_mean
    x, y = (
        df_mean.index,
        df_mean[y_col],
    )
    ci = 1.96 * df_std[y_col] / np.sqrt(n_seeds)
    plot_xy_ci(x, y, ci, x_col, y_col, save_path)


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
    df["color_ratio"] = df["points_per_color"].map(
        lambda ppc: ppc[0] / (ppc[0] + ppc[1])
    )  # ppc[0] assumed to be minority color
    os.makedirs(args.save_dir, exist_ok=True)
    plot_grouping(
        df,
        "color_ratio",
        "majority_share",
        os.path.join(args.save_dir, "color_ratio.png"),
    )
    plot_grouping(df, "k", "majority_share", os.path.join(args.save_dir, "k.png"))

    sub_df = df[df["use_subsampling"]]
    if len(sub_df) > 0:
        plot_grouping(
            df,
            "subsample_ratio",
            "majority_share",
            os.path.join(args.save_dir, "sub_ratio.png"),
        )
