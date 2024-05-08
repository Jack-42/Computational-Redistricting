import time
import matplotlib.pyplot as plt
import numpy as np
from iterative_ham import get_iterative_hs_cuts
from point_set import ColorPointSet

n = 12
points_per_color = (128, 128)
k_values = list(range(1, n))

num_iterations = 10 
average_execution_times = np.zeros(len(k_values))

for _ in range(num_iterations):
    execution_times = []

    for k in k_values:
        point_set = ColorPointSet(
            points_per_color=points_per_color,
            color_method="random",
        )

        start_time = time.time()
        _, _, _, _, _ = get_iterative_hs_cuts(point_set, k, True)
        end_time = time.time()

        execution_time = end_time - start_time
        execution_times.append(execution_time)

    average_execution_times += execution_times

average_execution_times /= num_iterations  

plt.plot(k_values, average_execution_times, marker="o")
plt.xlabel("k")
plt.ylabel("Average Execution Time (s)")
plt.title("Average Execution Time of Ham Sandwich Algorithm with Points per Color = 128")
plt.grid(True)
plt.show()
