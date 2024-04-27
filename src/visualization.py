"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Methods for visualizing colored point sets
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from utils.geometry import Line


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
    for l in lines:
        x1, y1 = l.p1.x, l.p1.y
        x2, y2 = l.p2.x, l.p2.y
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
            x1, y1 = line.p1.x, line.p1.y
            x2, y2 = line.p2.x, line.p2.y
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
        plt.legend(title="Cut Level", bbox_to_anchor=(1, 0.5), loc="center left")
        plt.tight_layout()
    _save_show(show, save_path)


def plot_point_set(
    point_set,
    show: bool = True,
    save_path=None,
    special_indices=None,
    plot_bbox: bool = False,
    hide_ticks: bool = False,
):
    cmap = list(mcolors.TABLEAU_COLORS.keys())
    if point_set.n_colors > len(cmap):
        raise NotImplementedError(
            f"Don't currently support visualizing more than {len(cmap)} colors"
        )
    colors = [cmap[c] for c in point_set.colors]
    # use opacity to mark special points (e.g., those on a cut-line)
    alpha_vals = np.ones(len(colors))
    if special_indices is not None and len(special_indices) > 0:
        alpha_vals[special_indices] = 0.5
    plt.scatter(point_set.x, point_set.y, c=colors, alpha=alpha_vals)
    if plot_bbox:
        plt.gca().add_patch(
            plt.Rectangle(
                (point_set.lower_x, point_set.lower_y),
                point_set.upper_x - point_set.lower_x,
                point_set.upper_y - point_set.lower_y,
                edgecolor="black",
                facecolor="none",
            )
        )
        # remove original frame
        for pos in ["right", "top", "bottom", "left"]:
            plt.gca().spines[pos].set_visible(False)
    if hide_ticks:
        plt.tick_params(
            left=False, right=False, labelleft=False, labelbottom=False, bottom=False
        )
    _save_show(show, save_path)
