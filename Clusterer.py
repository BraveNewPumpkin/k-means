import sys
import pandas as pd
from pathlib import Path
from random import randint
from pprint import pprint

from Point import Point
from Cluster import Cluster

usage = 'Clusterer.py number_of_clusters /path/to/input/dataset.csv /path/to/output/file'

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
    addPointsToClusters(points, clusters)
    pprint(clusters)


#    with output_data_path.open(mode='w') as output_data_stream:
#        data.to_csv(output_data_stream, index=False)

    return 0

def pointsFactory(data_frame):
    points = []
    for tuple in data_frame.itertuples():
        id_num = tuple[1]
        x = tuple[2]
        y = tuple[3]
        point = Point(id_num, x, y)
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
        index = randint(0, len(points))
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



    return distances


main(sys.argv)