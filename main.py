from random import randrange as random_value
from triangulation import delaunay_triangulation

lowestUniqueNodeId = 1
lowestUniqueEdgeId = 1

NODES_IN_AREA_LIMIT = 1000


# Function reads 3 arguments from standard input
def read_input() -> (int, int, int):
    numberOfNodesRaw = input()
    mapWidthRaw = input()
    mapHeightRaw = input()
    nameOfFileToStorePoints = input()
    nameOfFileToStoreRoads = input()

    return int(numberOfNodesRaw), int(mapWidthRaw), int(mapHeightRaw), nameOfFileToStorePoints, nameOfFileToStoreRoads


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
def connect_points_MST(pointsCollection: list[(int, int, int)]):
    delaunay_triangulation(pointsCollection)


# Fills given area with numberOfNodesToPut points, connects it and saves to file
def recursive_fill(areaWidth: int, areaHeight: int, leftBottomPoint: (int, int), numberOfNodesToPut: int):
    if numberOfNodesToPut <= NODES_IN_AREA_LIMIT:
        pointsCollection = generate_points_inside_area(areaWidth, areaHeight, leftBottomPoint, numberOfNodesToPut)

    else:
        print("not implemented yet")


if __name__ == '__main__':
    (numberOfNodes, mapWidth, mapHeight) = read_input()