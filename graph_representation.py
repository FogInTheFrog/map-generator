import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import pandas as pd


def draw_points(pointsCollection: list[int, int, int]):
    x_coordinates = []
    y_coordinates = []

    for name, x, y in pointsCollection:
        x_coordinates.append(x)
        y_coordinates.append(y)
    plt.plot(x_coordinates, y_coordinates, 'ro')
    plt.show()


def draw_points_with_convex_hull(pointsCollection: list[int, int, int],
                                 convexHullPointsCollection: list[int, int, int]):
    x_points = []
    y_points = []

    x_hull = []
    y_hull = []

    for name, x, y in pointsCollection:
        x_points.append(x)
        y_points.append(y)

    for name, x, y in convexHullPointsCollection:
        x_hull.append(x)
        y_hull.append(y)

    # We want to draw convex hull, so we need to add first point after last element
    # to make plt to draw line from first to last point of convex hull
    x_hull.append(convexHullPointsCollection[0][1])
    y_hull.append(convexHullPointsCollection[0][2])

    plt.plot(x_points, y_points, 'ro')
    plt.plot(x_hull, y_hull, color='r', linewidth=2.0)
    # plt.axis([-2, 12, -2, 12])
    plt.show()


def draw_points_and_edges(pointsCollection: list[(int, int, int, int)], edgesCollection: list[(int, int, int)]):
    x_points = []
    y_points = []

    pointsDict = dict()

    for pointId, x, y, h in pointsCollection:
        x_points.append(x)
        y_points.append(y)
        pointsDict[pointId] = (x, y)

    for weight, src, dest in edgesCollection:
        src_x, src_y = pointsDict[src]
        dest_x, dest_y = pointsDict[dest]
        plt.plot([src_x, dest_x], [src_y, dest_y], marker='o', color='r', linewidth=2.0)

    plt.show()


def draw_points_colormap(pointsCollection: list[(int, int, int, int)]):
    x_coordinates = []
    y_coordinates = []

    for name, x, y, h in pointsCollection:
        x_coordinates.append(x)
        y_coordinates.append(y)

    # Calculate the point density
    xy = np.vstack([x_coordinates, y_coordinates])
    z = gaussian_kde(xy)(xy)

    fig, ax = plt.subplots()
    ax.scatter(x_coordinates, y_coordinates, c=z, s=100)
    plt.show()


def draw_points_colormap_hist2d(pointsCollection: list[(int, int, int, int)]):
    x_coordinates = []
    y_coordinates = []

    for name, x, y, h in pointsCollection:
        x_coordinates.append(x)
        y_coordinates.append(y)

    plt.hist2d(x_coordinates, y_coordinates, (1500, 1500), cmap=plt.cm.jet)
    plt.colorbar()
    plt.show()


# value, x, y
def draw_points_depending_on_value(pointsCollection: list[(int, int, int, int)]):
    x_coordinates = []
    y_coordinates = []
    values = []

    for value, x, y, h in pointsCollection:
        x_coordinates.append(x)
        y_coordinates.append(y)
        values.append(value)

    df = pd.DataFrame({'x': x_coordinates,
                       'y': y_coordinates,
                       'z': values})

    print(len(x_coordinates), len(y_coordinates), len(values))
    plt.scatter(df.x, df.y, s=20, c=df.z, cmap='Greens')
    plt.show()
