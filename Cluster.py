from collections import defaultdict
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
        string = str(self.id_num) + '\t'
        string += ','.join(map(lambda point: str(point.id_num), self.points))
        return string

    def addPoint(self, point, distanceToCentroid):
        if point not in self.points:
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

        distances = defaultdict(list)
        for point1 in self.points:
            for point2 in self.points:
                distances[point1].append(point2.distanceTo(point1.text))

        total_dist = []
        for key in distances:
            total_dist.append(sum(distances[key]))

        min_dist = min(total_dist)
        min_dist_index = total_dist.index(min_dist)

        new_centroid = self.points[min_dist_index].id_num

        if self.centroid == new_centroid:
            return False
        self.centroid = new_centroid
        self.points = []
        self.distances_to_centroid = []
        return True
