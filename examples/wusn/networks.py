"""
# Filename: networks.py
# Description:
# Created by ngocjr7 on [12-06-2020 15:55:08]
"""
from __future__ import absolute_import
import sys, os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../../../geneticpython'))

from geneticpython.individual import Network
from collections import deque
from utils.input import WusnInput, WusnConstants
from utils.point import distance

from problems import SingleHopProblem

class SingleHopNetwork(Network):
    def __init__(self, problem : SingleHopProblem):
        self.m = problem._num_of_sensors
        self.n = problem._num_of_relays
        self.root = 0
        self.node_count = 1 + self.m + self.n
        self.edges = [set() for _ in range(self.node_count)]
        self.potential_edges = problem._edges
        self.parrent = [0 if (i > 0 and i <= self.n) else -1 for i in range(self.node_count)]
        self.node_types = problem._node_types
        self.idx2edge = problem._idx2edge
        self.edge2idx = problem._edge2idx
        self._points = problem._points

    def try_add_edge(self, i: int) -> bool: 
        u, v = self.idx2edge[i]
        if not (self.node_types[u] == 'relay' and self.node_types[v] == 'sensor'):
            return False
        
        if self.parrent[v] != -1: 
            return False
        
        return True

    def add_edge(self, i : int):
        u, v = self.idx2edge[i]
        self.edges[u].add(v)
        self.edges[v].add(u)
        self.parrent[v] = u

    def repair(self):
        self.num_used_relays = 0
        for i in range(1, self.n+1):
            if len(self.edges[i]) > 0:
                self.edges[i].add(0)
                self.edges[0].add(i)
                self.num_used_relays += 1
            else:
                self.parrent[i] = -1

        visited = [False] * self.node_count
        is_valid = True
        parrent = [-1] * self.node_count
        num_childs = [0] * self.node_count
        max_depth = 0

        def dfs(u : int, p : int, depth : int):
            ret = 1
            nonlocal max_depth
            visited[u] = True
            max_depth = max(max_depth, depth)

            for v in self.edges[u]:
                if v != p:
                    if visited[v]:
                        is_valid = False
                    else:
                        parrent[v] = u
                        ret += dfs(v, u, depth + 1)
            
            num_childs[u] = ret - 1
            return ret

        dfs(self.root, -1, 0)
        self.num_childs = num_childs

        is_valid &= (max_depth - 1 <= WusnConstants.hop)
        for i in range(self.n+1, self.n+self.m+1):
            is_valid &= visited[i]

        self.is_valid = is_valid

    def calc_max_energy_consumption(self):
        max_energy_consumption = 0

        for index in range(1, self.node_count):
            if self.parrent[index] != -1:
                e_t = WusnConstants.k_bit * WusnConstants.e_elec + \
                    WusnConstants.k_bit * WusnConstants.e_fs * distance(self._points[index], self._points[self.parrent[index]])
                e_r = WusnConstants.k_bit * WusnConstants.e_elec                

                e = (self.num_childs[index] + (index > self.n))*e_t + self.num_childs[index] * e_r + e_t
                
                e = self.num_childs[index] * e_r + \
                    (self.num_childs[index] + (index > self.n)) * WusnConstants.E_da + \
                    e_t

                max_energy_consumption = max(max_energy_consumption, e)
        return max_energy_consumption
