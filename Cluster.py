from itertools import count

from Tweet import Tweet


class Cluster(object):
    _id_counter = count(1)

    def __init__(self, centroid):
        self.id_num = next(self._id_counter)
        self.centroid = centroid
        self.points = []
        self.distances_to_centroid = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        string = str(self.id_num) + ' '
        string += ','.join(map(lambda point: str(point.tweet_id), self.points))
        return string

    def addPoint(self, point, distanceToCentroid):
        self.points.append(point)
        self.distances_to_centroid.append(distanceToCentroid)

    def calcSumOfSquareError(self):
        sum_squared_distance = 0
        for distance in self.distances_to_centroid:
            sum_squared_distance += pow(distance, 2)
        return sum_squared_distance

    # WARNING: this will delete points
    def attemptMoveCentroid(self):
        if len(self.points) == 0:
            return False

        avg_distance = sum(self.distances_to_centroid) / len(self.distances_to_centroid)

        distance_diff = list(map(lambda dist: abs(dist - avg_distance), self.distances_to_centroid))
        min_dist = min(distance_diff)
        min_dist_index = distance_diff.index(min_dist)

        new_centroid = self.points[min_dist_index].tweet_id

        if self.centroid == new_centroid:
            return False
        self.centroid = new_centroid
        self.points = []
        self.distances_to_centroid = []
        return True
