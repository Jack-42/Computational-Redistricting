"""
@author Jack Ringer, Anthony Sharma
Date: 4/13/2024
Description:
Jack's idea for voronoi sampling
"""

import numpy as np
from shapely import MultiPoint, Point, normalize
from shapely.ops import voronoi_diagram

from utils.constants import PERTURB_MAX

from point_set import ColorPointSet
from utils.dual import uw_dual_to_lines
from utils.geometry import Line, get_line_intersection

def get_voronoi_sample(point_set: ColorPointSet):
    #points = MultiPoint(point_set.x.ravel(),point_set.y.ravel())

    points = [(x, y) for x, y in zip(point_set.x, point_set.y)]

    regions = voronoi_diagram(MultiPoint(points))
    v_polygons = list(regions.geoms)
    lines = polygons_to_lines(polygons=v_polygons)
    return (point_set, lines)


def polygons_to_lines(polygons):
    lines = []
    for polygon in polygons:
        exterior_coords = list(polygon.exterior.coords)
        for i in range(len(exterior_coords) - 1):
            p1 = exterior_coords[i]
            p2 = exterior_coords[i + 1]
            lines.append(Line(p1=perturb_point(p1), p2=perturb_point(p2)))
    return lines

def perturb_point(point : tuple):    
    point_array = np.array(point)
    
    displacements = np.random.uniform(-PERTURB_MAX, PERTURB_MAX, size=point_array.shape)
    perturbed_point_array = point_array + displacements 
    
    return Point(perturbed_point_array)
