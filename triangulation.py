from random import randrange as random_value
from scipy.spatial import Delaunay, ConvexHull
import numpy as np

COPY_OPPOSITE_DIRECTION_TRI = False
COPY_OPPOSITE_DIRECTION_DSU = True
EXTRA_EDGE_CHANCE = (2, 4)  # for EXTRA_EDGE_CHANCE = (a, b) chance of adding this extra edges is a / b


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
            edges.append(edge_1)

            if COPY_OPPOSITE_DIRECTION_TRI:
                edge_2 = (euclidean_distance, pointsCollection[b][0], pointsCollection[a][0])
                edges.append(edge_2)

    return edges


def find_and_union(edges: list[(int, int, int)]):
    edges.sort()
    temp_points = set()

    for edge in edges:
        temp_points.add(edge[1])
        temp_points.add(edge[2])

    parent = dict(zip(temp_points, temp_points))
    rank = dict.fromkeys(temp_points, 0)

    result_edges = []

    def find(x):
        y = parent[x]
        if x == y:
            return x

        z = find(y)
        parent[x] = z
        return z

    def union(x, y):
        xRoot = find(x)
        yRoot = find(y)

        if xRoot == yRoot:
            (numerator, denominator) = EXTRA_EDGE_CHANCE
            chance = random_value(denominator)
            return chance < numerator

        xRootRank = rank[xRoot]
        yRootRank = rank[yRoot]

        if xRootRank > yRootRank:
            parent[yRoot] = xRoot
        else:
            parent[xRoot] = yRoot

            if xRootRank == yRootRank:
                rank[yRoot] += 1

        return True

    # Iterates edges and returns MST + potential extra edges with probability EXTRA_EDGE_CHANCE
    for weight, a, b in edges:
        if union(a, b):
            result_edges.append((weight, a, b))

            if COPY_OPPOSITE_DIRECTION_DSU:
                result_edges.append((weight, b, a))

    return result_edges


# Returns list of edges that belong to convex hull
def convex_hull(pointsCollection: list[int, int, int]) -> list[int, int, int]:
    points_temp = np.array([(x, y) for (name, x, y) in pointsCollection])
    hull = ConvexHull(points_temp)

    convexHullPoints = []
    convexHullEdges = []

    for point_id in hull.vertices:
        convexHullPoints.append(pointsCollection[point_id])
        if convexHullPoints.__len__() > 1:
            convexHullEdges.append()

    return result_points


# Returns list of edges that belong to convex hull
def convex_hull(pointsCollection: list[int, int, int]) -> list[int, int, int]:
    points_temp = np.array([(x, y) for (name, x, y) in pointsCollection])
    hull = ConvexHull(points_temp)

    convexHullPoints = []
    convexHullEdges = []

    for point_id in hull.vertices:
        convexHullPoints.append(pointsCollection[point_id])
        if convexHullPoints.__len__() > 1:
            convexHullEdges.append()

    return result_points
