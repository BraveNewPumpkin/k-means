from itertools import count

from Point import Point

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
        string = str(self.id_num ) + ' '
        string += ','.join(map(lambda point: str(point.id_num), self.points))
        return string

    def addPoint(self, point, distanceToCentroid):
        self.points.append(point)
        self.distances_to_centroid.append(distanceToCentroid)

    def calcSumOfSquareError(self):
        sum_squared_distance = 0
        for distance in self.distances_to_centroid:
           sum_squared_distance += pow(distance, 2)
        return sum_squared_distance

    #WARNING: this will delete points
    def attemptMoveCentroid(self):
        if(len(self.points) == 0):
            return False
        centroid_x = 0
        centroid_y = 0
        for point in self.points:
            centroid_x += point.x
            centroid_y += point.y
        centroid_x /= len(self.points)
        centroid_y /= len(self.points)
        new_centroid = Point(centroid_x, centroid_y)
        if self.centroid.isEqual(new_centroid):
            return False
        self.centroid = new_centroid
        self.points = []
        self.distances_to_centroid = []
        return True

