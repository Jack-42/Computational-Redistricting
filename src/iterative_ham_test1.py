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

n = 10
k_values = list(range(1, n))
points_per_color_values = [(2**i, 2**i) for i in range(1, n)]

num_iterations = 10 
average_execution_times = np.zeros((len(k_values), len(points_per_color_values)))

for _ in range(num_iterations):
    execution_times = []

    for k in k_values:
        for i, points_per_color in enumerate(points_per_color_values):
            if k > i + 1:
                execution_times.append(0)
                continue

            point_set = ColorPointSet(
                points_per_color=points_per_color,
                color_method="random",
            )

            start_time = time.time()
            np.random.seed(42)
            _, _, _, _, _ = get_iterative_hs_cuts(point_set, k, True)
            end_time = time.time()

            execution_time = end_time - start_time
            execution_times.append(execution_time)

    execution_times = np.array(execution_times).reshape(
        len(k_values), len(points_per_color_values)
    )
    average_execution_times += execution_times

average_execution_times /= num_iterations  

plt.figure()
plt.imshow(average_execution_times, cmap="viridis", origin="lower", interpolation="nearest")
plt.colorbar(label="Average Execution Time (s)")
plt.xlabel("Points per Color (start, end)")
plt.ylabel("k")
plt.xticks(np.arange(len(points_per_color_values)), points_per_color_values)
plt.yticks(np.arange(len(k_values)), k_values)
plt.title("Average Execution Time of Ham Sandwich Algorithm ({} Iterations)".format(num_iterations))
plt.grid(visible=False)
plt.show()
