from scipy.spatial import Delaunay
import numpy as np


# https://docs.scipy.org/doc/scipy/reference/tutorial/spatial.html
# Returns list of tuples where each tuple contains:
#       square of distance between point1 and point2 on euclidean plane,
#       point1.id,
#       point2.id
def delaunay_triangulation(pointsCollection: list[(int, int, int)]):
    edges = []
    points = np.array([(x, y) for (name, x, y) in pointsCollection])
    tri = Delaunay(points)
    for triangle in tri.simplices:
        for i in range(3):
            a = triangle[i]
            b = triangle[(i + 1) % 3]
            points_diff = points[a] - points[b]
            euclidean_distance = points_diff[0] ** 2 + points_diff[1] ** 2
            edge_1 = (euclidean_distance, pointsCollection[a][0], pointsCollection[b][0])
            edge_2 = (euclidean_distance, pointsCollection[b][0], pointsCollection[a][0])
            edges.append(edge_1)
            edges.append(edge_2)

    return edges
