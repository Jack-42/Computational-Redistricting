"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Class for generating/storing points in a 2D region.
Will sample and color the points according to the given parameters.
"""

import numpy as np

from constants import *


class ColorPointSet:
    def __init__(
        self,
        n_points: int,
        spatial_method: str,
        color_method: str,
        n_colors=2,
        color_probs=None,
        lower_x=0.0,
        upper_x=1.0,
        lower_y=0.0,
        upper_y=1.0,
    ) -> None:
        if color_probs is None:
            # give equal probability to each color
            color_probs = [1.0 / n_colors] * n_colors
        self.n_points = n_points
        self.spatial_method = spatial_method
        self.color_method = color_method
        self.n_colors = n_colors
        self.color_probs = color_probs
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
            color_sets[color] = np.column_stack(
                (
                    self.x[self.colors == color],
                    self.y[self.colors == color],
                )
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
        colors = np.random.choice(
            self.unique_colors, size=self.n_points, p=self.color_probs
        )
        return colors

    def __len__(self):
        return self.n_points
