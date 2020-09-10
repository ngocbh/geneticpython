"""
File: tree.py
Created by ngocjr7 on 2020-08-15 21:47
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""
from __future__ import absolute_import

from geneticpython.core.individual import Solution
from geneticpython.utils.validation import check_random_state
from typing import Callable
from copy import deepcopy
from collections import deque

from typing import Dict, List, NewType, Tuple, Union
import random
import numpy as np

EdgeList = NewType(
    "EdgeList", Union[List[Union[List[int], Tuple[int]]], Tuple[Union[List[int], Tuple[int]]]])


class Tree(Solution):
    initialization_methods = ['RandWalkRST', 'PrimRST', 'KruskalRST']

    def __init__(self, number_of_vertices: int, root: int = None, edge_list: EdgeList = None):
        if any(len(edge) != 2 for edge in edge_list):
            raise ValueError(
                "Each edge has to be a list or tuple containing 2 vertices. \
                For example: for two edges: 1-2, 2-3 --> [(1,2), (2,3)}]")
        if edge_list is None:
            self.edge_list = set()
            for i in range(number_of_vertices):
                for j in range(i):
                    self.edge_list.add((j, i))
            self.edge_list = list(self.edge_list)
        else:
            self.edge_list = set()
            for u, v in edge_list:
                if (u, v) not in self.edge_list and (v, u) not in self.edge_list:
                    self.edge_list.add((u, v))
            self.edge_list = list(self.edge_list)
        self.number_of_vertices = number_of_vertices
        self.root = root
        self.initialize()

    def initialize(self):
        self.adjacency = [set() for _ in range(self.number_of_vertices)]
        self.edges = set()

    def clone(self):
        return deepcopy(self)

    def get_adjacency(self):
        self.adjacency = [set() for _ in range(self.number_of_vertices)]
        for u, v in self.edges:
            self.adjacency[u].add(v)
            self.adjacency[v].add(u)

        return self.adjacency

    def find_path(self, source, destination):
        __visited = [False] * self.number_of_vertices
        path = []
        found = False

        def dfs(u, t, s):
            nonlocal found
            s.append(u)
            if u == t:
                nonlocal path
                path = list(s)
                found = True
            if found:
                return

            __visited[u] = True
            for v in self.adjacency[u]:
                if not __visited[v]:
                    dfs(v, t, s)
            s.pop()

        stack = deque()
        dfs(source, destination, stack)
        return path

    def try_add_edge(self, u: int, v: int) -> bool:
        raise NotImplementedError

    def add_edge(self, u: int, v: int) -> bool:
        raise NotImplementedError

    def check_validity(self) -> bool:
        __root = self.root or 0
        __visited = [False] * self.number_of_vertices

        def dfs(u):
            __visited[u] = True
            for v in self.adjacency[u]:
                if not __visited[v]:
                    dfs(v)

        dfs(__root)
        return len(self.edges) and all(__visited)

    def create_kruskal_rst(self, random_state=None):
        """random_init.

        Args:
            random_state:
        """
        random_state = check_random_state(random_state)
        # order = random_state.permutation(np.arange(len(self.edge_list)))
        weight = random_state.random(len(self.edge_list))
        order = np.argsort(-weight)
        self.initialize()
        for i in order:
            u, v = self.edge_list[i]
            if self.try_add_edge(u, v):
                self.add_edge(u, v)

        self.repair()


class KruskalTree(Tree):

    def initialize(self):
        super(KruskalTree, self).initialize()
        self.__kruskal_par = [i for i in range(self.number_of_vertices)]
        self.__rank = [0] * self.number_of_vertices

    def find(self, u: int):
        if self.__kruskal_par[u] != u:
            self.__kruskal_par[u] = self.find(self.__kruskal_par[u])

        return self.__kruskal_par[u]

    def union(self, u: int, v: int):
        uroot = self.find(u)
        vroot = self.find(v)

        if self.__rank[uroot] < self.__rank[vroot]:
            self.__kruskal_par[uroot] = vroot
        elif self.__rank[uroot] > self.__rank[vroot]:
            self.__kruskal_par[vroot] = uroot
        else:
            self.__kruskal_par[vroot] = uroot
            self.__rank[uroot] += 1

    def try_add_edge(self, u: int, v: int) -> bool:
        uroot = self.find(u)
        vroot = self.find(v)
        return (uroot != vroot)

    def add_edge(self, u: int, v: int):
        if not self.try_add_edge(u, v):
            return False
        self.union(u, v)
        self.adjacency[u].add(v)
        self.adjacency[v].add(u)
        self.edges.add((u, v))
        return True


class RootedTree(Tree):
    def __init__(self, number_of_vertices: int, root: int, edge_list: EdgeList = None):
        if root is None or root < 0 or root >= number_of_vertices:
            raise ValueError(
                "Invalid root param, requires 0 <= root < number_of_vertices")

        super(RootedTree, self).__init__(number_of_vertices, root, edge_list)

    def initialize(self):
        super(RootedTree, self).initialize()
        self.parent = [-1] * self.number_of_vertices
        self.parent[self.root] = self.root

    def try_add_edge(self, u: int, v: int) -> bool:
        return (self.parent[u] == -1) ^ (self.parent[v] == -1)

    def add_edge(self, u: int, v: int) -> bool:
        if not self.try_add_edge(u, v):
            return False
        if self.parent[u] == -1:
            self.parent[u] = v
        else:
            self.parent[v] = u
        self.adjacency[u].add(v)
        self.adjacency[v].add(u)
        self.edges.add((u, v))
        return True


class LinkCutTree(Tree):
    def initialize(self):
        raise NotImplementedError

    def link(self, u: int, v: int):
        raise NotImplementedError

    def cut(self, u: int, v: int):
        raise NotImplementedError
