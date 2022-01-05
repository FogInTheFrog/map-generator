import copy
from random import randrange as random_value
from random import getrandbits
from triangulation import delaunay_triangulation, find_and_union, convex_hull, \
    convex_hull_points_to_edges, get_edges_when_points_collinear, are_points_collinear, \
    find_center_of_polygon, get_square_of_distance, distance_between_two_points_including_height
from graph_representation import draw_points_and_edges, draw_points, draw_points_colormap, draw_points_colormap_hist2d
from altitude_generator import generate_mountain_ranges, calculate_height

lowestUniqueNodeId = 1
lowestUniqueEdgeId = 1

VERTICAL_NUMBER_OF_REGIONS = 512
HORIZONTAL_NUMBER_OF_REGIONS = 512
REGION_HEIGHT = 320
REGION_WIDTH = 320

POPULATION_DENSITY_MIN = 1 / 6
STARTING_POINT = (0, 0)
DEBUG = False


# Function reads 3 arguments from standard input
def read_input() -> (str, str):
    nameOfFileToStorePointsRaw = input()
    nameOfFileToStoreRoadsRaw = input()

    return nameOfFileToStorePointsRaw, nameOfFileToStoreRoadsRaw


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
                                numberOfNodesToPut: int, mountainRanges) -> list[(int, int, int, int)]:
    uniqueCoordinatesCollection = set()
    while uniqueCoordinatesCollection.__len__() < numberOfNodesToPut:
        x_vec = random_value(areaWidth)
        y_vec = random_value(areaHeight)

        if (x_vec, y_vec) not in uniqueCoordinatesCollection:
            uniqueCoordinatesCollection.add((x_vec, y_vec))

    pointsCollection = []
    for (x, y) in uniqueCoordinatesCollection:
        point_id = get_new_node_id()
        height = calculate_height(mountainRanges, (leftBottomPoint[0] + x, leftBottomPoint[1] + y))
        point = (point_id, leftBottomPoint[0] + x, leftBottomPoint[1] + y, height)
        pointsCollection.append(point)

    return pointsCollection


# In the plane, the Euclidean minimum spanning tree is a subgraph of the Delaunay triangulation. Using this fact,
# the Euclidean minimum spanning tree for a given set of planar points may be found in time
# O(n log n), using algorithms based on comparisons of simple combinations of input coordinates.
def connect_points_EMST_with_extra_edges(pointsCollection: list[(int, int, int, int)]):
    if are_points_collinear(pointsCollection):
        pointsCollectionCopy = copy.copy(pointsCollection)
        potential_edges = get_edges_when_points_collinear(pointsCollectionCopy)
        return potential_edges
    else:
        potential_edges = delaunay_triangulation(pointsCollection)
        return find_and_union(potential_edges)


# edges = list[(weight, src, dest)]
def save_edges_to_file(edges: list[(int, int, int)], nameOfFile: str):
    # TODO generowanie nazw
    with open(nameOfFile, 'a') as file:
        for edge in edges:
            (weight, src, dest) = edge
            edge_id = get_new_edge_id()
            separator = ","
            file.write(str(src) + separator + str(dest) + separator +
                       str(weight) + separator + str(edge_id) + "\n")


# pointsCollection = list[(point_id, x, y)]
def save_points_to_file(pointsCollection: list[(int, int, int)], nameOfFile: str):
    # TODO generowanie nazw
    with open(nameOfFile, 'a') as file:
        for point in pointsCollection:
            (point_id, x, y) = (point[0], point[1], point[2])
            separator = ","
            file.write(str(point_id) + separator + str(x) + separator + str(y) + "\n")


# Returns number of points between two points with one same coordinate
def get_distance_1d(a: int, b: int):
    return abs(b - a) + 1


# Limits regions size to populate region with given density
def find_region_limits(numberOfPoints: int) -> (int, int, int, int):
    regionLeft = 0
    regionRight = REGION_WIDTH - 1
    regionBot = 0
    regionTop = REGION_HEIGHT - 1

    # Returns new region horizontal / vertical ranges
    def get_half(regionMin: int, regionMax: int, chooseSmallerCoordinatesHalf: bool) -> (int, int):
        mid = (regionMin + regionMax) // 2

        if chooseSmallerCoordinatesHalf:
            return regionMin, mid
        return mid + 1, regionMax

    def calculate_density() -> float:
        area = ((regionRight - regionLeft + 1) * (regionTop - regionBot + 1))
        density = numberOfPoints / area
        if DEBUG:
            print(numberOfPoints, area, density)

        return density

    def is_possible_to_shorten(regionMin: int, regionMax: int):
        return get_distance_1d(regionMin, regionMax) > 2

    def is_possible_to_shorten_any() -> bool:
        return is_possible_to_shorten(regionLeft, regionRight) or \
               is_possible_to_shorten(regionBot, regionTop)

    densityOfCurrentRegion = calculate_density()

    while is_possible_to_shorten_any() and densityOfCurrentRegion <= POPULATION_DENSITY_MIN:
        # Decision whether to cut horizontally or vertically depends on which axis is greater
        # Randomizes if both values are equal
        toShortenVertically = bool(getrandbits(1))
        distanceVertically = get_distance_1d(regionTop, regionBot)
        distanceHorizontally = get_distance_1d(regionLeft, regionRight)
        if distanceHorizontally < distanceVertically:
            toShortenVertically = True
        elif distanceHorizontally > distanceVertically:
            toShortenVertically = False

        toChooseSmallerHalf = bool(getrandbits(1))

        if toShortenVertically and is_possible_to_shorten(regionBot, regionTop):
            regionBot, regionTop = get_half(regionBot, regionTop, toChooseSmallerHalf)
        else:
            regionLeft, regionRight = get_half(regionLeft, regionRight, toChooseSmallerHalf)
        densityOfCurrentRegion = calculate_density()

    return regionLeft, regionRight, regionBot, regionTop


# Returns shift vector depending on regionId
def calculate_shift_for_region(regionId: int):
    regionColumn = (regionId - 1) % HORIZONTAL_NUMBER_OF_REGIONS + 1
    regionRow = ((regionId - 1) // HORIZONTAL_NUMBER_OF_REGIONS) + 1
    xShift = (regionColumn - 1) * REGION_WIDTH
    yShift = (regionRow - 1) * REGION_HEIGHT
    return xShift, yShift


# Fills given area with numberOfNodesToPut points, connects it and saves to file
def populate_region(regionId: int, numberOfNodesToPut: int, nameOfFileToStorePoints: str,
                    nameOfFileToStoreRoads: str, mountainRanges):
    regionLeft, regionRight, regionBot, regionTop = find_region_limits(numberOfNodesToPut)
    areaWidth = get_distance_1d(regionRight, regionLeft)
    areaHeight = get_distance_1d(regionTop, regionBot)
    xShift, yShift = calculate_shift_for_region(regionId)
    leftBottomPoint = (xShift + regionLeft, yShift + regionBot)

    # pointsCollection is a list consisting tuples like (pointId, x, y, height)
    pointsCollection = generate_points_inside_area(areaWidth, areaHeight, leftBottomPoint, numberOfNodesToPut,
                                                   mountainRanges)

    edges = connect_points_EMST_with_extra_edges(pointsCollection)

    convexHullPointsCollection = convex_hull(pointsCollection)
    convexHullEdges = convex_hull_points_to_edges(convexHullPointsCollection)

    if DEBUG:
        draw_points_and_edges(pointsCollection, edges)
        draw_points_and_edges(pointsCollection, edges + convexHullEdges)

    save_points_to_file(pointsCollection, nameOfFileToStorePoints)
    save_edges_to_file(edges, nameOfFileToStoreRoads)

    return convexHullPointsCollection, convexHullEdges


def connect_regions(centralPoints: list[(int, int, int, int)], convexHullsOfRegions: list[list[(int, int, int, int)]]):
    def find_closest_point(aPointsOnConvexHull: list[(int, int, int, int)],
                           bPointsOnConvexHull: list[(int, int, int, int)]):
        a = aPointsOnConvexHull[0]
        b = bPointsOnConvexHull[0]
        bestResult = distance_between_two_points_including_height(a, b)

        for my_a in aPointsOnConvexHull:
            for my_b in bPointsOnConvexHull:
                dist = distance_between_two_points_including_height(my_a, my_b)
                if dist < bestResult:
                    a = my_a
                    b = my_b
                    bestResult = dist

        return a, b, bestResult

    potential_edges = connect_points_EMST_with_extra_edges(centralPoints)
    edges = []

    for (weight, src, dest) in potential_edges:
        aPointsCollection = convexHullsOfRegions[src - 1]
        bPointsCollection = convexHullsOfRegions[dest - 1]

        (point_a, point_b, distance) = find_closest_point(aPointsCollection, bPointsCollection)
        edges.append((distance, point_a[0], point_b[0]))

    return edges


def randomize_number_of_points_in_region() -> int:
    x = random_value(1, 31041)
    if x == 1:
        return random_value(10000, 30000)
    elif 2 <= x <= 6:
        return random_value(5000, 10000)
    elif 7 <= x <= 16:
        return random_value(3000, 5000)
    elif 17 <= x <= 41:
        return random_value(2000, 4000)
    elif 42 <= x <= 241:
        return random_value(500, 2000)
    elif 242 <= x <= 441:
        return random_value(200, 500)
    elif 442 <= x <= 1042:
        return random_value(50, 200)
    else:
        return random_value(5, 50)


if __name__ == '__main__':
    (nameOfFileToStorePoints, nameOfFileToStoreRoads) = read_input()
    numberOfRegions = HORIZONTAL_NUMBER_OF_REGIONS * VERTICAL_NUMBER_OF_REGIONS
    sumOfAllPoints = 0
    pointsCollectionFromConvexHulls = []
    centralPointsFromConvexHulls = []

    MAP_WIDTH = HORIZONTAL_NUMBER_OF_REGIONS * REGION_WIDTH
    MAP_HEIGHT = VERTICAL_NUMBER_OF_REGIONS * REGION_HEIGHT
    mountains = generate_mountain_ranges(10, MAP_WIDTH, MAP_HEIGHT)

    for regionId in range(1, numberOfRegions + 1):
        pointsInRegion = randomize_number_of_points_in_region()
        sumOfAllPoints += pointsInRegion

        pointsConvexHull, edgesConvexHull = populate_region(regionId, pointsInRegion, nameOfFileToStorePoints,
                                                            nameOfFileToStoreRoads, mountains)

        pointsCollectionFromConvexHulls.append(pointsConvexHull)

        centerOfConvexHull = find_center_of_polygon(regionId, pointsConvexHull)
        centralPointsFromConvexHulls.append(centerOfConvexHull)

    highways = connect_regions(centralPointsFromConvexHulls, pointsCollectionFromConvexHulls)

    save_edges_to_file(highways, nameOfFileToStoreRoads)

    # Printing:
    print(sumOfAllPoints)

    # flatPointsCollectionFromConvexHulls = [point for sublist in pointsCollectionFromConvexHulls for point in sublist]
    #
    # draw_points_and_edges(flatPointsCollectionFromConvexHulls, edgesCUL + highways)
    # draw_points_colormap_hist2d(flatPointsCollectionFromConvexHulls)
