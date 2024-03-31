"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Methods for visualizing colored point sets
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


def plot_points(point_set, save_path=None):
    cmap = list(mcolors.TABLEAU_COLORS.keys())
    if point_set.n_colors > len(cmap):
        raise NotImplementedError(
            f"Don't currently support visualizing more than {len(cmap)} colors"
        )
    colors = [cmap[c] for c in point_set.colors]
    plt.scatter(point_set.x, point_set.y, c=colors)
    if save_path is not None:
        plt.savefig(save_path, dpi=300)
    plt.show()
