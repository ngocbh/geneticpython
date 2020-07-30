"""
# Filename: networks.py
# Description:
# Created by ngocjr7 on [12-06-2020 15:55:08]
"""
from __future__ import absolute_import
import sys, os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../../../geneticpython'))

from geneticpython.core.individual import Network
from collections import deque
from utils.input import WusnInput, WusnConstants
from utils.point import distance

from problems import SingleHopProblem, MultiHopProblem

class WusnNetwork(Network):
    def __init__(self, problem : MultiHopProblem):
        self.m = problem._num_of_sensors
        self.n = problem._num_of_relays
        self.root = 0
        self.node_count = 1 + self.m + self.n
        self.potential_edges = problem._edges
        self.node_types = problem._node_types
        self.idx2edge = problem._idx2edge
        self.edge2idx = problem._edge2idx
        self._points = problem._points
        self.num_encoded_edges = problem._num_encoded_edges

        self.init_solution()

    def init_solution(self):
        self.rank = [0] * self.node_count
        self.kruskal_par = [i for i in range(self.node_count)]
        self.edges = [set() for _ in range(self.node_count)]
        self.parent = [-1 for i in range(self.node_count)]
        self.num_childs = [0 for i in range(self.node_count)]
        self.num_used_relays = 0
        self.is_valid = True

        for i in range(1, self.n+1):
            self.union(0, i)
            self.edges[0].add(i)
            self.edges[i].add(0)

    def find(self, u : int):
        if self.kruskal_par[u] != u:
            self.kruskal_par[u] = self.find(self.kruskal_par[u])
        
        return self.kruskal_par[u]

    def union(self, u : int, v : int):
        uroot = self.find(u)
        vroot = self.find(v)

        if self.rank[uroot] < self.rank[vroot]:
            self.kruskal_par[uroot] = vroot
        elif self.rank[uroot] > self.rank[vroot]:
            self.kruskal_par[vroot] = uroot
        else:
            self.kruskal_par[vroot] = uroot
            self.rank[uroot] += 1

    def try_add_edge(self, i : int) -> bool:
        u, v = self.idx2edge[i]
        uroot = self.find(u)
        vroot = self.find(v)
        return (uroot != vroot)

    def add_edge(self, i):
        u, v = self.idx2edge[i]
        self.union(u, v)
        self.edges[u].add(v)
        self.edges[v].add(u)

    def repair(self):
        visited = [False] * self.node_count
        is_valid = True
        parent = [-1] * self.node_count
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
                        parent[v] = u
                        ret += dfs(v, u, depth + 1)
            
            num_childs[u] = ret - 1
            return ret

        dfs(self.root, -1, 0)
        self.num_childs = num_childs
        self.parent = parent

        self.num_used_relays = self.n
        for i in range(1, self.n + 1):
            if self.num_childs[i] == 0:
                self.num_used_relays -= 1
                self.parent[i] = -1
                self.num_childs[0] -= 1

        is_valid &= (max_depth - 1 <= WusnConstants.hop)
        self.max_depth = max_depth
        for i in range(self.n+1, self.n+self.m+1):
            is_valid &= visited[i]

        self.is_valid = is_valid
    
    def calc_max_energy_consumption(self):
        max_energy_consumption = 0

        for index in range(1, self.node_count):
            if self.parent[index] != -1:
                e_t = WusnConstants.k_bit * WusnConstants.e_elec + \
                    WusnConstants.k_bit * WusnConstants.e_fs * distance(self._points[index], self._points[self.parent[index]])
                e_r = WusnConstants.k_bit * WusnConstants.e_elec                

                e = (self.num_childs[index] + (index > self.n))*e_t + self.num_childs[index] * e_r + e_t
                
                e = self.num_childs[index] * e_r + \
                    (self.num_childs[index] + (index > self.n)) * WusnConstants.E_da + \
                    e_t

                max_energy_consumption = max(max_energy_consumption, e)
        
        return max_energy_consumption




