"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Methods for visualizing colored point sets
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from sympy import Line, Point


def _save_show(show: bool, save_path):
    if save_path is not None:
        plt.savefig(save_path, dpi=300)
    if show:
        plt.show()


def plot_lines(
    lines: list[Line],
    show: bool = True,
    save_path=None,
    color: str = "r",
):
    for i in range(len(lines)):
        p1, p2 = lines[i].points
        x1, y1 = float(p1[0]), float(p1[1])
        x2, y2 = float(p2[0]), float(p2[1])
        plt.axline((x1, y1), (x2, y2), color=color)
    _save_show(show, save_path)


def plot_k_cuts(
    cut_lines: dict[int, Line],
    k: int,
    segments_only: bool = False,
    show: bool = True,
    save_path=None,
    colors: list[str] = None,
    labels: list[str] = None,
):
    if colors is None:
        # want to show each level in diff color, use a continuous colorspace
        cmap = plt.cm.get_cmap("winter")
        cmap_colors = [cmap(i) for i in np.linspace(0, 1, k)]
        colors = cmap_colors[:k]
        labels = np.arange(1, k + 1)
    for level in cut_lines.keys():
        first_l = True  # needed because matplotlib can't identify unique labels
        for line in cut_lines[level]:
            p1, p2 = line.points
            x1, y1 = float(p1[0]), float(p1[1])
            x2, y2 = float(p2[0]), float(p2[1])
            if labels is not None and first_l:
                label = labels[level]
                first_l = False
            else:
                label = None
            if segments_only:
                plt.plot([x1, x2], [y1, y2], color=colors[level], label=label)
            else:
                plt.axline((x1, y1), (x2, y2), color=colors[level], label=label)
    if labels is not None:
        plt.legend(title="Cut Level")
    _save_show(show, save_path)


def plot_point_set(point_set, show: bool = True, save_path=None):
    cmap = list(mcolors.TABLEAU_COLORS.keys())
    if point_set.n_colors > len(cmap):
        raise NotImplementedError(
            f"Don't currently support visualizing more than {len(cmap)} colors"
        )
    colors = [cmap[c] for c in point_set.colors]
    plt.scatter(point_set.x, point_set.y, c=colors)
    _save_show(show, save_path)
