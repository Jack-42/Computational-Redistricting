import time
import matplotlib.pyplot as plt
import numpy as np
from iterative_ham import get_iterative_hs_cuts
from point_set import ColorPointSet

n = 7
k = 4
points_per_color_values = [2**i for i in range(4, n + 4)]  # starting points_per_color at 16

num_iterations = 10  
average_execution_times = []

for _ in range(num_iterations):
    execution_times = []

    for points_per_color in points_per_color_values:
        point_set = ColorPointSet(
            points_per_color=(points_per_color, points_per_color),
            color_method="random",
        )

        start_time = time.time()
        _, _, _, _, _ = get_iterative_hs_cuts(point_set, k, True)
        end_time = time.time()

        execution_time = end_time - start_time
        execution_times.append(execution_time)

    average_execution_times.append(execution_times)

average_execution_times = np.mean(average_execution_times, axis=0) 

plt.plot(points_per_color_values, average_execution_times, marker="o")
plt.xscale("log")  
plt.yscale("log") 
plt.xlabel("Points per Color")
plt.ylabel("Average Execution Time (s)")
plt.title("Average Execution Time of Ham Sandwich Algorithm with k = 4")
plt.grid(True)
plt.show()