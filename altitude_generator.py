
from random import randrange as random_value, uniform
from graph_representation import draw_points_and_edges, draw_points_depending_on_value
import math
import numpy as np
from numpy.linalg import norm


def is_point_on_map(x: int, y: int, map_width: int, map_height: int) -> bool:
    return 0 <= x <= map_width and 0 <= y <= map_height


def generate_mountain_ranges(numberOfMountains: int, map_width: int, map_height: int) -> list[((int, int), (int, int))]:
    listOfMountainsExtremities = []
    mountainLength = 35000             # units
    mountainWidth = 3500               # units
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for i in range(numberOfMountains):
        (x, y) = random_value(0, map_width), random_value(0, map_height)
        vector = uniform(0, 2 * math.pi)
        (s, t) = (mountainLength, 0)

        deltaX = int(s * math.cos(vector) + t * math.sin(vector))
        deltaY = int(-s * math.sin(vector) + t * math.cos(vector))

        for (dirX, dirY) in directions:
            newX = x + dirX * deltaX
            newY = y + dirY * deltaY

            if is_point_on_map(newX, newY, map_width, map_height):
                listOfMountainsExtremities.append(((x, y), (newX, newY)))
                break

    return listOfMountainsExtremities


def calculate_height(mountainRange, point):
    src, dest = mountainRange
    return np.abs(np.cross(dest-src, src-point)) / norm(dest-src)


def sample_points_for_heatmap(mountainRanges, mapHeight, mapWidth):
    pointsCollection = []
    for i in range(0, mapWidth, 200):
        for j in range(0, mapHeight, 200):
            height = 0
            for (srcX, srcY), (destX, destY) in mountainRanges:
                diffSrc = int(math.sqrt((srcX - i) ** 2 + (srcY - j) ** 2))
                diffDest = int(math.sqrt((destX - i) ** 2 + (destY - j) ** 2))
                diff = min(diffSrc, diffDest)
                # We calculate factor and percentile to match this:
                # https://pl.wikipedia.org/wiki/Geografia_Polski#/media/Plik:Profil_wysoko%C5%9Bciowy_Polski.svg
                # {{0,0},{0.2,100},{0.75,200},{0.9,300},{0.95, 400}, {0.975, 600}, {0.99, 900}, {1, 2500}}
                factor = min(max((35000 - diff) / 35000, 0), 1)  # or 35000 TODO: this
                percentile = factor ** 3  # TODO: change to 20
                height += int(percentile * 25)
            print(height, end=' ')
            pointsCollection.append((height, i, j))

    draw_points_depending_on_value(pointsCollection)


if __name__ == '__main__':
    MAP_WIDTH = 512 * 320
    MAP_HEIGHT = 512 * 320
    mountains = generate_mountain_ranges(10, MAP_WIDTH, MAP_HEIGHT)
    points = []
    edges = []
    ctr = 0
    for (a, b), (c, d) in mountains:
        ctr += 1
        points.append((ctr, a, b))
        ctr += 1
        points.append((ctr, c, d))
        edges.append((ctr, ctr - 1, ctr))

    draw_points_and_edges(points, edges)
    print(mountains)
    sample_points_for_heatmap(mountains, MAP_WIDTH, MAP_HEIGHT)
