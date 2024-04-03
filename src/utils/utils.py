"""
@author Jack Ringer, Anthony Sharma
Date: 4/2/2024
Description: Generic utilities
"""

import numpy as np
from sympy import Point


def xy_to_points(x: np.ndarray, y: np.ndarray) -> list[Point]:
    return list(map(lambda coords: Point(*coords), zip(x, y)))
