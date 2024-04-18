import time
import matplotlib.pyplot as plt

from iterative_ham import get_iterative_hs_cuts
from point_set import ColorPointSet


n = 7  
k = 4 

points_per_color_values = [2**i for i in range(4, n + 4)]  # starting points_per_color at 16

execution_times = []

for points_per_color in points_per_color_values:
    point_set = ColorPointSet(
        points_per_color=(points_per_color, points_per_color),
        spatial_method='random',
        color_method='random'
    )

    start_time = time.time()
    cuts, cut_segments, points_on_cuts, err = get_iterative_hs_cuts(point_set, k)
    end_time = time.time()
    
    execution_time = end_time - start_time
    execution_times.append(execution_time)

plt.plot(points_per_color_values, execution_times, marker='o')
plt.xscale('log')  # Use a logarithmic scale for better visualization
plt.xlabel('Points per Color')
plt.ylabel('Execution Time (s)')
plt.title('Execution Time of Ham Sandwich Algorithm with k = 4')
plt.grid(True)
plt.show()
