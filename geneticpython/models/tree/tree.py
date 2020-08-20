"""
File: tree.py
Created by ngocjr7 on 2020-08-15 21:47
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""
from __future__ import absolute_import

from geneticpython.core.individual import Solution
from typing import Callable

class Tree(Solution):
    def __init__(self, number_of_vertices: int, root: int = None):
        self.number_of_vertices = number_of_vertices
        self.root = root
        self.initialize()

    def initialize(self):
        self.adjacency = [set() for _ in range(self.number_of_vertices)]
        self.edges = set()

    def get_adjacency(self):
        self.adjacency = [set() for _ in range(self.number_of_vertices)]
        for u, v in self.edges:
            self.adjacency[u].add(v)
            self.adjacency[v].add(u)

        return self.adjacency

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


class LinkCutTree(Tree):
    def initialize(self):
        raise NotImplementedError

    def link(self, u : int, v : int):
        raise NotImplementedError

    def cut(self, u : int, v : int):
        raise NotImplementedError
