from __future__ import absolute_import

from collections import defaultdict

from .point import SensorNode, RelayNode, Point

import json
import math
import os
import pickle

class WusnConstants:
    # Unit: J
    e_elec = 50 * 1e-9
    e_fs = 10 * 1e-12
    e_mp = 0.0013 * 1e-12
    e_da = 5 * 1e-12

    # Num of bits
    k_bit = 4000

    # hop constraint
    hop = 6

    E_da = e_da * k_bit


class WusnInput:
    def __init__(self, _W=500, _H=500, _depth=1., _height=10., _num_of_relays=10, _num_of_sensors=50,
                 _radius=20., _relays=None, _sensors=None, _BS=None):
        self.W = _W
        self.H = _H
        self.depth = _depth
        self.height = _height
        self.relays = _relays
        self.sensors = _sensors
        self.num_of_relays = _num_of_relays
        self.num_of_sensors = _num_of_sensors
        self.radius = _radius
        self.BS = _BS

    @classmethod
    def from_file(cls, path):
        f = open(path)
        d = json.load(f)
        return cls.from_dict(d)

    @classmethod
    def from_dict(cls, d):
        W = d['W']
        H = d['H']
        depth = d['depth']
        height = d['height']
        num_of_relays = d['num_of_relays']
        num_of_sensors = d['num_of_sensors']
        radius = d['radius']
        relays = []
        sensors = []
        BS = Point.from_dict(d['center'])
        for i in range(num_of_sensors):
            sensors.append(SensorNode.from_dict(d['sensors'][i]))
        for i in range(num_of_relays):
            relays.append(RelayNode.from_dict(d['relays'][i]))

        return cls(W, H, depth, height, num_of_relays, num_of_sensors, radius, relays, sensors, BS)

    def freeze(self):
        self.sensors = tuple(self.sensors)
        self.relays = tuple(self.relays)

    def to_dict(self):
        return {
            'W': self.W, 'H': self.H,
            'depth': self.depth, 'height': self.height,
            'num_of_relays': self.num_of_relays,
            'num_of_sensors': self.num_of_sensors,
            'relays': list(map(lambda x: x.to_dict(), self.relays)),
            'sensors': list(map(lambda x: x.to_dict(), self.sensors)),
            'center': self.BS.to_dict(),
            'radius': self.radius
        }

    def to_file(self, file_path):
        d = self.to_dict()
        with open(file_path, "wt") as f:
            fstr = json.dumps(d, indent=4)
            f.write(fstr)

    def __hash__(self):
        return hash((self.W, self.H, self.depth, self.height, self.num_of_relays, self.num_of_sensors, self.radius,
                     tuple(self.relays), tuple(self.sensors)))

    def __eq__(self, other):
        return hash(self) == hash(other)


if __name__ == "__main__":
    inp = WusnInput.from_file('./data/small_data/dem1_0.in')
    print(inp.relays[0])