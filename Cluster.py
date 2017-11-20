from itertools import count
class Cluster(object):
    _id_counter = count(1)
    def __init__(self, centroid):
        self.id_num = next(self._id_counter)
        self.centroid = centroid
        self.points = []
        self.distancesToCentroid = []
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        string = str(self.id_num ) + ' '
        string += ','.join(map(lambda point: str(point.id_num), self.points))
        return string

    def addPoint(self, point, distanceToCentroid):
        self.points.append(point)
        self.distancesToCentroid.append(distanceToCentroid)

