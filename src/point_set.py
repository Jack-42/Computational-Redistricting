"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Class for generating/storing points in a 2D region.
Will sample and color the points according to the given parameters.
"""

from typing import Optional

import numpy as np
from shapely import Polygon

from utils.constants import *
from utils.geometry import get_vertices, xy_to_points
from utils.weighting import get_biased_weights_random


class ColorPointSet:
    def __init__(
        self,
        points_per_color: list[int] = None,
        spatial_method: str = None,
        color_method: str = None,
        weighting_method: str = None,
        k: int = 1,
        spreads: np.ndarray = None,
        color_sets: Optional[dict] = None,
        defining_poly: Optional[Polygon] = None,
    ) -> None:
        self.lower_x = LOWER_X
        self.upper_x = UPPER_X
        self.lower_y = LOWER_Y
        self.upper_y = UPPER_Y

        if color_sets is not None and defining_poly is not None:
            self._alt_init(color_sets, defining_poly)
            return

        self.n_points = sum(points_per_color)
        self.spatial_method = spatial_method
        self.color_method = color_method
        self.n_colors = len(points_per_color)
        self.points_per_color = points_per_color

        self.x, self.y = self._uniform_random()
        self.is_weight = np.zeros(
            len(self.x), dtype="bool"
        )  # is_weight[i] == if point i is just a "weight"
        # colors[i] = m indicates point (x[i], y[i]) is color m, m in [0, n_colors]
        self.unique_colors = np.arange(self.n_colors)
        self.colors = self._get_point_colors()
        self.points = xy_to_points(self.x, self.y)
        self.color_sets = self._get_color_sets()
        self.og_color_sets = self.color_sets
        if weighting_method is not None and weighting_method == BIASED_WEIGHT:
            n_regions = 2**k
            self.weights = get_biased_weights_random(
                self.colors, points_per_color, n_regions
            )
            # even spread
            spreads = [0.01] * len(self.weights)
            self.spreads = np.array(spreads)
            self._cluster()
        elif weighting_method is not None and weighting_method == POPULATION_WEIGHT:
            # TODO:
            raise NotImplementedError()

    def _alt_init(self, color_sets: dict, defining_poly: Polygon):
        # don't need all attributes if using this initialization
        self.color_sets = color_sets
        self.n_colors = len(color_sets)
        self.n_points = sum([len(c_set) for c_set in color_sets.values()])

        # defining_poly contains all points, so can just these vertices to calculate bounds
        vertices = get_vertices(defining_poly)
        self.lower_x = min(vertices, key=lambda p: p.x).x
        self.upper_x = max(vertices, key=lambda p: p.x).x
        self.lower_y = min(vertices, key=lambda p: p.y).y
        self.upper_y = max(vertices, key=lambda p: p.y).y

    def get_matching_indices(self, query_ps: list, atol: float = 1e-8) -> np.ndarray:
        """
        Used for helping visualize/set opacity of points on cut-line
        """
        indices = []
        for p in query_ps:
            for i, (x_val, y_val) in enumerate(zip(self.x, self.y)):
                if np.isclose(p.x, x_val, atol=atol) and np.isclose(
                    p.y, y_val, atol=atol
                ):
                    indices.append(i)
        return np.array(indices)

    def _get_color_sets(self):
        # colors_lists[i] = (x[j], y[j]) where color[j]=i
        color_sets = {}
        for color in self.unique_colors:
            idx = self.colors == color
            color_sets[color] = xy_to_points(self.x[idx], self.y[idx])
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

    def _cluster(self) -> tuple[np.ndarray, np.ndarray]:
        x = self.x
        y = self.y
        w = self.weights - 1  # -1 to not double-count original point
        d = self.spreads
        colors = self.colors

        new_x = np.empty(np.sum(w))
        new_y = np.empty(np.sum(w))
        new_colors = np.empty(np.sum(w), dtype=int)
        self.weighted_to_og = {}  # maps weighted points to their original point
        self.og_to_weighted = {}  # maps original points to their weighted points

        j_offset = self.n_points

        j = 0
        for i, (xi, yi, wi, di) in enumerate(zip(x, y, w, d)):
            for _ in range(wi):
                r = di * np.sqrt(np.random.rand())

                theta = np.random.uniform(0, 2 * np.pi)

                x_new = xi + r * np.cos(theta)
                y_new = yi + r * np.sin(theta)

                new_x[j] = x_new
                new_y[j] = y_new
                new_colors[j] = colors[i]

                self.og_to_weighted[i] = self.og_to_weighted.get(i, []) + [j_offset + j]
                self.weighted_to_og[j_offset + j] = i

                j += 1

        new_is_weight = np.ones(len(new_colors), dtype="bool")
        self.is_weight = np.append(self.is_weight, new_is_weight)
        self.colors = np.append(self.colors, new_colors)
        self.x = np.append(self.x, new_x)
        self.y = np.append(self.y, new_y)
        self.points = xy_to_points(self.x, self.y)
        self.n_points = len(x)
        unique, counts = np.unique(self.colors, return_counts=True)
        self.points_per_color = np.zeros(len(unique))
        for u, c in zip(unique, counts):
            self.points_per_color[u] = c
        self.color_sets = self._get_color_sets()

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
