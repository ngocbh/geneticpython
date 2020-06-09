from __future__ import absolute_import

import math

class Point:
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d['x'], d['y'], d['z'])

    def __repr__(self):
        return '%s(%f %f %f)' % (self.__class__.__name__, self.x, self.y, self.z)


class SensorNode(Point):
    def __init__(self, _x, _y, _z):
        super().__init__(_x, _y, _z)


class RelayNode(Point):
    def __init__(self, _x, _y, _z):
        super().__init__(_x, _y, _z)


def distance(p1: Point, p2: Point):
    return math.sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2) + pow(p1.z - p2.z, 2))


if __name__ == "__main__":
    p1 = RelayNode(1, 1, 1)
    p2 = SensorNode(2, 2, 2)
    print(distance(p1, p2))