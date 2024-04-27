"""
@author Jack Ringer, Anthony Sharma
Date: 3/31/2024
Description: Contains constant values used throughout project
"""

import numpy as np

# algorithm options
HAM_SANDWICH = "ham_sandwich"
ITERATIVE_HAM_SANDWICH = "iterative_ham_sandwich"
VISUALIZE_POINTS = "visualize_points"
VORONOI_SAMPLING = "voronoi_sampling"

# sampling methods
UNIFORM_RANDOM = "uni_random"

# color sampling methods
RANDOM = "random"

# weighting
UNIFORM_WEIGHT = "uni_weight"
BIASED_WEIGHT = "bias_weight"

# math
EPSILON = np.finfo(np.float64).eps

# define domain
# be careful that points are in general position for small domain if using random sampling
LOWER_X = -10.0
UPPER_X = 10.0
LOWER_Y = -10.0
UPPER_Y = 10.0

# perturb amount
PERTURB_MAX = 0.0001
