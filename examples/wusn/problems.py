"""
# Filename: problems.py
# Description:
# Created by ngocjr7 on [12-06-2020 14:27:21]
"""
from __future__ import absolute_import

from collections import deque
from utils.input import WusnInput, WusnConstants
from utils.point import distance

class SingleHopProblem():
    def __init__(self, inp : WusnInput):
        self._sensors = inp.sensors
        self._relays = inp.relays
        self._radius = inp.radius
        self._num_of_sensors = inp.num_of_sensors
        self._num_of_relays = inp.num_of_relays

        self._hop = WusnConstants.hop

        self.graph_construct(inp)

    def graph_construct(self, inp: WusnInput):
        point2idx = {}
        points = []
        point2idx[inp.BS] = 0
        node_types = ['base']

        points.append(inp.BS)
        for i, rl in enumerate(inp.relays):
            point2idx[rl] = i + 1
            points.append(rl)
            node_types.append('relay')
        for i, sn in enumerate(inp.sensors):
            point2idx[sn] = i + 1 + inp.num_of_relays
            points.append(sn)
            node_types.append('sensor')

        # Construct edge set
        edges = [[] for _ in range(len(points))]

        for i in range(inp.num_of_relays):
            edges[0].append(i)
            edges[i].append(0)
        
        self._num_encoded_edges = 0
        self._edge2idx = dict()
        self._idx2edge = list()

        for rl in inp.relays:
            for sn in inp.sensors:
                if distance(rl, sn) <= inp.radius:
                    u, v = point2idx[rl], point2idx[sn]
                    edges[u].append(v)
                    edges[v].append(u)

                    self._edge2idx[u,v] = self._num_encoded_edges
                    self._edge2idx[v,u] = self._num_encoded_edges
                    self._idx2edge.append((u,v))
                    self._num_encoded_edges += 1

        self._points = points
        self._point2idx = point2idx
        self._edges = edges
        self._node_types = node_types



class MultiHopProblem():
    def __init__(self, inp : WusnInput):
        pass