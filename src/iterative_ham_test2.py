import time
import matplotlib.pyplot as plt

from iterative_ham import get_iterative_hs_cuts
from point_set import ColorPointSet


n = 11  
points_per_color = (128,128)

k_values = list(range(1, n))

execution_times = []

for k in k_values:
    point_set = ColorPointSet(
        points_per_color=points_per_color,
        spatial_method='random',
        color_method='random'
    )

    start_time = time.time()
    cuts, cut_segments, points_on_cuts, err = get_iterative_hs_cuts(point_set, k)
    end_time = time.time()
    
    execution_time = end_time - start_time
    execution_times.append(execution_time)

plt.plot(k_values, execution_times, marker='o')
plt.xlabel('k')
plt.ylabel('Execution Time (s)')
plt.title('Execution Time of Ham Sandwich Algorithm with Points per Color = 128')
plt.grid(True)
plt.show()
