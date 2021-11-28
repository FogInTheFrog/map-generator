from scipy.spatial import Delaunay
import numpy as np


def delaunay_triangulation(coordinates):
    points = np.array((x, y) for (name, x, y) in coordinates)
    tri = Delaunay(points)
    print(tri)
