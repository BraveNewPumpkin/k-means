class Point(object):
    def __init__(self, x, y, id_num=None):
        self.id_num = id_num
        self.x = x
        self.y = y

    def __str__(self):
        string = 'x: ' + str(self.x) + ', y: ' + str(self.y)
        return string

    def __repr__(self):
        string = '(x: ' + str(self.x) + ', y: ' + str(self.y) + ')'
        return string

    def distanceTo(self, other_point):
        return pow(pow(other_point.x - self.x, 2) + pow(other_point.y - self.y, 2), .5)

    def isEqual(self, other_point):
        return self.x == other_point.x and self.y == other_point.y
