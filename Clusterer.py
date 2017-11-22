import sys
import pandas as pd
from matplotlib import pyplot
from pathlib import Path
from random import randint
from itertools import count
from pprint import pprint

from Point import Point
from Cluster import Cluster

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
    points = pointsFactory(data_frame=data)
    centroids = chooseCentroids(number_of_clusters=number_of_clusters, points=points)
    clusters = createClusters(centroids)

    pyplot.close('all')
    figure = pyplot.figure()

    iterator = count(2)
    is_finished = False
    iteration_number = 1
    while not is_finished and not iteration_number > MAX_ITERATIONS:
        print('-' * 80, '\n', 'iteration number: ', iteration_number)
        addPointsToClusters(points, clusters)
        pprint(clusters)
        sum_of_squares_error = calcSumOfSquareError(clusters)
        print('sum of squares error:', sum_of_squares_error)
        num_moved = 0
        for cluster in clusters:
            if cluster.attemptMoveCentroid():
                num_moved += 1
        is_finished = num_moved == 0

        num_axes = len(figure.axes)
        num_columns = 5
        new_num_subplots = num_axes + 1
        new_num_rows = calcRowNumber(plot_number=new_num_subplots, num_subplots_per_row=num_columns)
        for i in range(num_axes):
            plot_number = i + 1
            figure.axes[i].change_geometry(new_num_rows, num_columns, plot_number)
        new_subplot = figure.add_subplot(new_num_rows, num_columns, new_num_subplots)
        new_subplot.set_title('iteration ' + str(iteration_number))
        for cluster in clusters:
            x = cluster.getXValues()
            y = cluster.getYValues()
            new_subplot.plot(x, y, 'o')
        iteration_number = next(iterator)
    figure.subplots_adjust(wspace=0.9, hspace=0.9)
    pyplot.show()
    #    with output_data_path.open(mode='w') as output_data_stream:
    #        data.to_csv(output_data_stream, index=False)

    return 0

def calcRowNumber(plot_number, num_subplots_per_row):
    return (plot_number - 1) // num_subplots_per_row + 1

def calcColumnNumber(plot_number, num_subplots_per_row):
    return (plot_number - 1) % num_subplots_per_row + 1

def pointsFactory(data_frame):
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
    for i in range(0, number_of_clusters):
        index = randint(0, len(points) - 1)
        centroid_points.append(points[index])
    return centroid_points


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
