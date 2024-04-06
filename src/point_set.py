"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Class for generating/storing points in a 2D region.
Will sample and color the points according to the given parameters.
"""

import numpy as np

from utils.constants import *
from utils.utils import xy_to_points


class ColorPointSet:
    def __init__(
        self,
        points_per_color: list[int],
        spatial_method: str,
        color_method: str,
        lower_x=0.0,
        upper_x=1.0,
        lower_y=0.0,
        upper_y=1.0,
    ) -> None:
        self.n_points = sum(points_per_color)
        self.spatial_method = spatial_method
        self.color_method = color_method
        self.n_colors = len(points_per_color)
        self.points_per_color = points_per_color
        self.lower_x = lower_x
        self.upper_x = upper_x
        self.lower_y = lower_y
        self.upper_y = upper_y

        self.x, self.y = self._get_sample_points()
        # colors[i] = m indicates point (x[i], y[i]) is color m, m in [0, n_colors
        self.unique_colors = np.arange(self.n_colors)
        self.colors = self._get_point_colors()
        self.color_sets = self._get_color_sets()

    def _get_color_sets(self):
        # colors_lists[i] = (x[j], y[j]) where color[j]=i
        color_sets = {}
        for color in self.unique_colors:
            color_sets[color] = xy_to_points(
                self.x[self.colors == color], self.y[self.colors == color]
            )
        self.color_sets = color_sets
        return color_sets

    def _get_sample_points(self) -> tuple[np.ndarray, np.ndarray]:
        if self.spatial_method == UNIFORM_RANDOM:
            return self._uniform_random()
        else:
            raise NotImplementedError(
                f"Given spatial_method not supported: {self.spatial_method}"
            )

    def _get_point_colors(self) -> np.ndarray:
        if self.color_method == RANDOM:
            return self._random_colors()
        else:
            raise NotImplementedError(
                f"Given color_method not supported: {self.color_method}"
            )

    def _uniform_random(self) -> tuple[np.ndarray, np.ndarray]:
        x = np.random.uniform(self.lower_x, self.upper_x, self.n_points)
        y = np.random.uniform(self.lower_y, self.upper_y, self.n_points)
        return x, y

    def _random_colors(self) -> np.ndarray:
        # for random case this is overly complicated, but want code to be adapatable
        # to other color-sampling techniques (e.g., based on location)
        colors = []
        for i, n in enumerate(self.points_per_color):
            i_arr = [i] * n
            colors.extend(i_arr)
        colors = np.array(colors)
        return np.array(colors)

    def __len__(self):
        return self.n_points
