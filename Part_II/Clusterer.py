import sys
import pandas as pd
from pathlib import Path
from itertools import count
from pprint import pprint

from Tweet import Tweet
from Cluster import Cluster

usage = 'Clusterer.py number_of_clusters /path/to/input/InitialSeeds.txt /path/to/input/Tweets.json /path/to/output/file'
MAX_ITERATIONS = 25

if len(sys.argv) < 5:
    print('not enough arguments\n')
    print(usage)
    sys.exit(1)
if len(sys.argv) > 5:
    print('too many arguments\n')
    print(usage)
    sys.exit(1)


def main(argv):
    number_of_clusters = int(argv[1])
    input_data_path = Path(argv[3])
    initial_seeds_path = Path(argv[2])
    output_data_path = Path(argv[4])

    # Read Tweet id and text
    data = pd.read_json(input_data_path, lines=True)[['id', 'text']]

    # Create a dictionary with tweet_id as the key
    tweet_dict = data.set_index('text').groupby('id').apply(lambda df: df.index.tolist()).to_dict()

    points = createTweets(data_frame=data)

    # Initial centroids
    seeds = (pd.read_csv(initial_seeds_path, names=['a', 'b'])).iloc[:, 0]
    if number_of_clusters > len(seeds):
        print('The value of k must be less than', len(seeds))
        sys.exit(1)
    centroids = chooseCentroids(number_of_clusters=number_of_clusters, seeds=seeds)

    # Initialize clusters
    clusters = createClusters(centroids)

    iterator = count(2)
    is_finished = False
    iteration_number = 1
    while not is_finished and not iteration_number > MAX_ITERATIONS:
        print('-' * 80, '\n')
        iteration_string = 'iteration number: ' + str(iteration_number)
        print(iteration_string)
        addPointsToClusters(points=points, clusters=clusters, tweet_dict=tweet_dict)
        pprint(clusters)
        sum_of_squares_error = calcSumOfSquareError(clusters)
        print('sum of squares error:', sum_of_squares_error)
        num_moved = 0
        for cluster in clusters:
            if cluster.attemptMoveCentroid():
                num_moved += 1
        is_finished = num_moved == 0
        iteration_number = next(iterator)
    #    with output_data_path.open(mode='w') as output_data_stream:
    #        data.to_csv(output_data_stream, index=False)

    return 0

def createTweets(data_frame):
    tweets = []
    for tuple in data_frame.itertuples():
        tweet_id = tuple[1]
        text = tuple[2]
        tweet = Tweet(tweet_id, text)
        tweets.append(tweet)
    return tweets


def createClusters(centroids):
    clusters = []
    for centroid in centroids:
        clusters.append(Cluster(centroid=centroid))
    return clusters


def chooseCentroids(number_of_clusters, seeds):
    return seeds.sample(number_of_clusters)

def addPointsToClusters(points, clusters, tweet_dict):
    for point in points:
        distances = []
        for cluster in clusters:
            distances.append(point.distanceTo(''.join(tweet_dict[cluster.centroid])))
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
