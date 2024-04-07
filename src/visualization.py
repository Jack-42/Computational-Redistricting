"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Methods for visualizing colored point sets
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from sympy import Line, Point


def _save_show(show: bool, save_path):
    if save_path is not None:
        plt.savefig(save_path, dpi=300)
    if show:
        plt.show()


def plot_lines(
    lines: list[Line],
    segments_only: bool = False,
    show: bool = True,
    save_path=None,
    color: str = "gold",
):
    # there's probably a better way to do this
    for line in lines:
        p1, p2 = line.points
        x1, y1 = float(p1[0]), float(p1[1])
        x2, y2 = float(p2[0]), float(p2[1])
        if segments_only:
            plt.plot([x1, x2], [y1, y2], color=color)
        else:
            plt.axline((x1, y1), (x2, y2), color=color)
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
