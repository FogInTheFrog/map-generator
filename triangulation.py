from random import randrange as random_value
from scipy.spatial import Delaunay, ConvexHull
import numpy as np

COPY_OPPOSITE_DIRECTION_TRI = False     # Triangulation
COPY_OPPOSITE_DIRECTION_DSU = False     # Disjoint set union
COPY_OPPOSITE_DIRECTION_CHU = False     # Convex Hull


# Should be used before trying to triangulate and calculate convex hull
def are_points_collinear(pointsCollection: list[(int, int, int)]) -> bool:
    if pointsCollection.__len__() < 3:
        return True

    a = pointsCollection[0]
    b = pointsCollection[1]
    x1_vec = a[1] - b[1]
    y1_vec = a[2] - b[2]

    def are_three_points_collinear(c: (int, int, int)) -> bool:
        x2_vec = a[1] - c[1]
        y2_vec = a[2] - c[2]
        return x1_vec * y2_vec == x2_vec * y1_vec

    for i in range(2, pointsCollection.__len__()):
        if not are_three_points_collinear(pointsCollection[i]):
            return False

    return True


# Calculates chance of adding extra edge depending on numberOfPoints
# Return type is a pair (a, b) where chance is a / b
# NOTE: According to our observations the best proportion is:
#       1/4 extra edge chance and (1/3 to 1/4) density
def extra_edge_chance_formula(numberOfPoints: int) -> (int, int):
    return 1, 3


def get_square_of_distance(pointA: (int, int), pointB: (int, int)):
    diff = (pointB[0] - pointA[0]), (pointB[1] - pointA[1])
    return diff[0] ** 2 + diff[1] ** 2


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


# Returns list of (weight, src, dest)
def find_and_union(edges: list[(int, int, int)]):
    edges.sort()
    temp_points = set()
    extraEdgeChance = extra_edge_chance_formula(edges.__len__())

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
            (numerator, denominator) = extraEdgeChance
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


# Function should be used only when points are collinear
# Returns list of tuples where each tuple contains:
#       square of distance between point1 and point2 on euclidean plane,
#       point1.id,
#       point2.id
def get_edges_when_points_collinear(pointsCollection: list[(int, int, int)]):
    pointsCollection.sort(key=lambda y: (y[1], y[2]))
    edges = []

    for i in range(1, pointsCollection.__len__()):
        a = pointsCollection[i - 1]
        b = pointsCollection[i]
        squareEuclideanDist = ((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2)
        edge_1 = (squareEuclideanDist, a[0], b[0])
        edges.append(edge_1)

        if COPY_OPPOSITE_DIRECTION_TRI:
            edge_2 = (squareEuclideanDist, b[0], a[0])
            edges.append(edge_2)

    return edges


# Returns list of points that belong to convex hull
def convex_hull(pointsCollection: list[(int, int, int)]) -> list[(int, int, int)]:
    if are_points_collinear(pointsCollection):
        return pointsCollection

    result_points = []
    points_temp = np.array([(x, y) for (name, x, y) in pointsCollection])
    hull = ConvexHull(points_temp)

    for point_id in hull.vertices:
        result_points.append(pointsCollection[point_id])

    return result_points


# Returns list of edges that belong to convex hull
def convex_hull_points_to_edges(pointsCollection: list[(int, int, int)]) -> list[(int, int, int)]:
    convexHullEdges = []
    n = pointsCollection.__len__()

    for i in range(n):
        (pointId1, x1, y1) = pointsCollection[i]
        (pointId2, x2, y2) = pointsCollection[(i + 1) % n]
        euclidean_distance = (x1 - x2) ** 2 + (y1 - y2) ** 2
        convexHullEdges.append((euclidean_distance, pointId1, pointId2))

        if COPY_OPPOSITE_DIRECTION_CHU:
            convexHullEdges.append((euclidean_distance, pointId2, pointId1))

    return convexHullEdges


def find_center_of_polygon(regionId: int, pointsCollection: list[(int, int, int)]) -> (int, int):
    numOfPoints = pointsCollection.__len__()
    x_mean = sum(point[1] for point in pointsCollection) // numOfPoints
    y_mean = sum(point[2] for point in pointsCollection) // numOfPoints

    return regionId, x_mean, y_mean
