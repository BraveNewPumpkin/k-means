import sys
import pandas as pd
import random
from pathlib import Path
from itertools import count
from copy import deepcopy
from pprint import pprint

from Point import Point
from Cluster import Cluster
from Plot import Plot
from Plotter import Plotter

usage = 'Clusterer.py number_of_clusters /path/to/input/dataset.csv /path/to/output/file'
MAX_ITERATIONS = 25

if len(sys.argv) < 4:
    print('not enough arguments\n')
    print(usage)
    sys.exit(1)
if len(sys.argv) > 4:
    print('too many arguments\n')
    print(usage)
    sys.exit(1)


def main(argv):
    number_of_clusters = int(argv[1])
    input_data_path = Path(argv[2])
    output_data_path = Path(argv[3])

    data = pd.read_csv(filepath_or_buffer=input_data_path, delim_whitespace=True)
    points = createPoints(data_frame=data)
    centroids = chooseCentroids(number_of_clusters=number_of_clusters, points=points)
    clusters = createClusters(centroids)

    plotter = Plotter(num_columns=5, num_clusters=number_of_clusters)

    iterator = count(2)
    is_finished = False
    iteration_number = 1
    while not is_finished and not iteration_number > MAX_ITERATIONS:
        print('-' * 80, '\n')
        iteration_string = 'iteration number: ' + str(iteration_number)
        print(iteration_string)
        addPointsToClusters(points, clusters)
        pprint(clusters)
        sum_of_squares_error = calcSumOfSquareError(clusters)
        print('sum of squares error:', sum_of_squares_error)
        plot = Plot(label=iteration_string, clusters=deepcopy(clusters))
        plotter.addPlot(plot)
        num_moved = 0
        for cluster in clusters:
            if cluster.attemptMoveCentroid():
                num_moved += 1
        is_finished = num_moved == 0
        iteration_number = next(iterator)
    plotter.show()
    #    with output_data_path.open(mode='w') as output_data_stream:
    #        data.to_csv(output_data_stream, index=False)

    return 0

def createPoints(data_frame):
    points = []
    for tuple in data_frame.itertuples():
        id_num = tuple[1]
        x = tuple[2]
        y = tuple[3]
        point = Point(x, y, id_num)
        points.append(point)
    return points


def createClusters(centroids):
    clusters = []
    for centroid in centroids:
        clusters.append(Cluster(centroid=centroid))
    return clusters


def chooseCentroids(number_of_clusters, points):
    centroid_points = []
    ranges = fathomRanges(points)
    for i in range(0, number_of_clusters):
        x_min = ranges['x_min']
        y_min = ranges['y_min']
        x_max = ranges['x_max']
        y_max = ranges['y_max']
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        centroid_points.append(Point(x=x, y=y))
    return centroid_points

def fathomRanges(points):
    if len(points) > 0:
        x_max = points[0].x
        x_min = points[0].x
        y_max = points[0].y
        y_min = points[0].y
    for point in points:
       if x_max < point.x:
           x_max = point.x
       if x_min > point.x:
           x_min = point.x
       if y_max < point.y:
           y_max = point.y
       if y_min > point.y:
           y_min = point.y
    return {'x_max': x_max, 'x_min': x_min, 'y_max': y_max, 'y_min': y_min}

def addPointsToClusters(points, clusters):
    for point in points:
        distances = []
        for cluster in clusters:
            distances.append(point.distanceTo(cluster.centroid))
        min_distance = min(distances)
        min_distance_index = distances.index(min_distance)
        clusters[min_distance_index].addPoint(point, min_distance)
    return clusters


def calcSumOfSquareError(clusters):
    sum_squared_distance = 0
    for cluster in clusters:
        sum_squared_distance += cluster.calcSumOfSquareError()
    return sum_squared_distance


main(sys.argv)
