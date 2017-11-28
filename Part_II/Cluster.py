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
        if point not in self.points:
            self.points.append(point)
            self.distances_to_centroid.append(distanceToCentroid)

    def calcSumOfSquareError(self):
        sum_squared_distance = 0
        for distance in self.distances_to_centroid:
            sum_squared_distance += pow(distance, 2)
        return sum_squared_distance

    def getXValues(self):
        return list(map(lambda point: point.x, self.points))

    def getYValues(self):
        return list(map(lambda point: point.y, self.points))

    # WARNING: this will delete points
    def attemptMoveCentroid(self):
        if len(self.points) == 0:
            return False

        distances = dict()
        for point1 in self.points:
            distances[point1] = list(map(lambda point2: point2.distanceTo(point1.text), self.points))

        total_dist = []
        for key in distances:
            total_dist.append(sum(distances[key]))

        min_dist = min(total_dist)
        min_dist_index = total_dist.index(min_dist)

        new_centroid = self.points[min_dist_index].tweet_id

        if self.centroid == new_centroid:
            return False
        self.centroid = new_centroid
        self.points = []
        self.distances_to_centroid = []
        return True
