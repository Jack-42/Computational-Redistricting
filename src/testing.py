"""
@author Jack Ringer, Anthony Sharma
Date: 4/15/2024
Description: Testing run times
"""

import time

import matplotlib.pyplot as plt
import numpy as np

from iterative_ham import get_iterative_hs_cuts
from point_set import ColorPointSet

n = 8
k_values = list(range(1, n))
points_per_color_values = [(2**i, 2**i) for i in range(1, n)]

execution_times = []

for k in k_values:
    for i, points_per_color in enumerate(points_per_color_values):

        if k > i + 1:
            execution_times.append(0)
            continue

        point_set = ColorPointSet(
            points_per_color=points_per_color,
            spatial_method="random",
            color_method="random",
        )

        start_time = time.time()
        np.random.seed(42)
        cuts, cut_segments, points_on_cuts, err = get_iterative_hs_cuts(point_set, k)
        end_time = time.time()

        execution_time = end_time - start_time
        execution_times.append(execution_time)


execution_times = np.array(execution_times).reshape(
    len(k_values), len(points_per_color_values)
)

plt.figure()
plt.imshow(execution_times, cmap="viridis", origin="lower", interpolation="nearest")
plt.colorbar(label="Execution Time (s)")
plt.xlabel("Points per Color (start, end)")
plt.ylabel("k")
plt.xticks(np.arange(len(points_per_color_values)), points_per_color_values)
plt.yticks(np.arange(len(execution_times)), range(1, len(execution_times) + 1))
plt.title("Execution Time of Ham Sandwich Algorithm")
plt.grid(visible=False)
plt.show()
