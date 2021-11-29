from random import randrange as random_value
from triangulation import delaunay_triangulation, find_and_union, convex_hull
from graph_representation import draw_points_with_convex_hull

lowestUniqueNodeId = 1
lowestUniqueEdgeId = 1

NODES_IN_AREA_LIMIT = 1000
STARTING_POINT = (0, 0)


# Function reads 3 arguments from standard input
def read_input() -> (int, int, int):
    numberOfNodesRaw = input()
    mapWidthRaw = input()
    mapHeightRaw = input()
    nameOfFileToStorePointsRaw = input()
    nameOfFileToStoreRoadsRaw = input()

    return int(numberOfNodesRaw), int(mapWidthRaw), int(mapHeightRaw), \
           nameOfFileToStorePointsRaw, nameOfFileToStoreRoadsRaw


# Function returns lowest unique id of point
def get_new_node_id() -> int:
    global lowestUniqueNodeId
    lowestUniqueNodeId += 1
    return lowestUniqueNodeId - 1


# Function returns lowest unique id of road
def get_new_edge_id() -> int:
    global lowestUniqueEdgeId
    lowestUniqueEdgeId += 1
    return lowestUniqueEdgeId - 1


# Generates random coordinates for numberOfNodes inside given area
# For given coordinates (x, y) of leftBottomPoint and area width and height,
# function generates integer coordinates in range [x; x + width - 1] and [y; y + height - 1]
def generate_points_inside_area(areaWidth: int, areaHeight: int, leftBottomPoint: (int, int),
                                numberOfNodesToPut: int) -> list[(int, int, int)]:
    uniqueCoordinatesCollection = set()
    while uniqueCoordinatesCollection.__len__() < numberOfNodesToPut:
        x_vec = random_value(areaWidth)
        y_vec = random_value(areaHeight)

        if (x_vec, y_vec) not in uniqueCoordinatesCollection:
            uniqueCoordinatesCollection.add((x_vec, y_vec))

    pointsCollection = []
    for (x, y) in uniqueCoordinatesCollection:
        point_id = get_new_node_id()
        point = (point_id, leftBottomPoint[0] + x, leftBottomPoint[1] + y)
        pointsCollection.append(point)

    return pointsCollection


# In the plane, the Euclidean minimum spanning tree is a subgraph of the Delaunay triangulation. Using this fact,
# the Euclidean minimum spanning tree for a given set of planar points may be found in time
# O(n log n), using algorithms based on comparisons of simple combinations of input coordinates.
def connect_points_EMST_with_extra_edges(pointsCollection: list[(int, int, int)]):
    potential_edges = delaunay_triangulation(pointsCollection)
    return find_and_union(potential_edges)


# Fills given area with numberOfNodesToPut points, connects it and saves to file
def recursive_fill(areaWidth: int, areaHeight: int, leftBottomPoint: (int, int), numberOfNodesToPut: int):
    if numberOfNodesToPut <= NODES_IN_AREA_LIMIT:
        pointsCollection = generate_points_inside_area(areaWidth, areaHeight, leftBottomPoint, numberOfNodesToPut)
        edges = connect_points_EMST_with_extra_edges(pointsCollection)
        convexHullEdges = convex_hull(pointsCollection)
        # draw_points(pointsCollection)
        draw_points_with_convex_hull(pointsCollection, hullPointsCollection)
    else:
        print("not implemented yet")


if __name__ == '__main__':
    (numberOfNodes, mapWidth, mapHeight, nameOfFileToStorePoints, nameOfFileToStoreRoads) = read_input()
    recursive_fill(mapWidth, mapHeight, STARTING_POINT, numberOfNodes)
