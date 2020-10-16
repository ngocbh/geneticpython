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
from geneticpython.utils import rset
from typing import Callable
from copy import deepcopy
from collections import deque

from typing import Dict, List, NewType, Tuple, Union
import random
import numpy as np

EdgeList = NewType(
    "EdgeList", Union[List[Union[List[int], Tuple[int]]], Tuple[Union[List[int], Tuple[int]]]])


class Tree(Solution):
    initialization_methods = ['RandWalkRST', 'PrimRST']

    def __init__(self, number_of_vertices: int,
                 root: int = None,
                 potential_edges: EdgeList = None,
                 init_method: str = 'RandWalkRST'):
        if potential_edges is not None and any(len(edge) != 2 for edge in potential_edges):
            raise ValueError(
                "Each edge has to be a list or tuple containing 2 vertices. \
                For example: for two edges: 1-2, 2-3 --> [(1,2), (2,3)}]")

        self.number_of_vertices = number_of_vertices
        self.root = root

        self.potential_edges = set()
        self.potential_adj = [list() for _ in range(number_of_vertices)]
        if potential_edges is None:
            for i in range(number_of_vertices):
                for j in range(i):
                    self.potential_edges.add((j, i))
                    self.potential_adj[i].append(j)
                    self.potential_adj[j].append(i)

            self.potential_edges = list(self.potential_edges)
        else:
            for u, v in potential_edges:
                if (u, v) not in self.potential_edges and (v, u) not in self.potential_edges:
                    self.potential_edges.add((u, v))
                    self.potential_adj[u].append(v)
                    self.potential_adj[v].append(u)
            self.potential_edges = list(self.potential_edges)

        self.set_initialization_method(init_method)
        self.initialize()

    def initialize(self):
        self.adjacency = [list() for _ in range(self.number_of_vertices)]
        self.edges = list()

    def clone(self):
        return deepcopy(self)

    def get_adjacency(self, edges=None):
        __edges = edges or self.edges
        adjacency = [list() for _ in range(self.number_of_vertices)]
        for u, v in __edges:
            adjacency[u].append(v)
            adjacency[v].append(u)

        if edges is None:
            self.adjacency = adjacency.copy()
        return adjacency

    def get_potential_adj(self):
        self.potential_adj = self.get_adjacency(self.potential_edges)
        return self.potential_adj

    def random_init(self, random_state=None):
        if self._initialization_method == 'RandWalkRST':
            self.create_random_walk_rst(random_state)
        elif self._initialization_method == 'PrimRST':
            self.create_prim_rst(random_state)

    def set_initialization_method(self, method: str):
        """set_initialization_method.

        Args:
            method (str): method
        """
        if method not in self.initialization_methods:
            raise ValueError(
                f"Invalid initialization method, only accept {self.initialization_methods}")
        self._initialization_method = method

    def create_prim_rst(self, random_state=None):
        random_state = check_random_state(random_state)
        if self.root is not None:
            root = self.root
        else:
            random_state.randint(0, self.number_of_vertices)

        self.initialize()
        if len(self.edges) != 0:
            raise Exception('Default random init on Tree only accept empty Tree at initialization.\n\
                            Donot add_edge at initialize() or try other random init function.')
        # Set of connected nodes
        C = set()
        # eligible edges
        A = rset() # my implementation of set that helps get random in set in O(1)

        # Init tree
        C.add(root)
        for v in self.potential_adj[root]:
            A.add((root, v))

        while len(C) < self.number_of_vertices:
            u, v = A.random_choice(random_state)
            A.remove((u, v))

            if v not in C:
                self.add_edge(u, v)
                C.add(v)
                for w in self.potential_adj[v]:
                    if w not in C:
                        A.add((v, w))

            if len(A) == 0:
                raise ValueError('Cannot create random spanning tree from unconnected tree')
        self.repair()

    def create_random_walk_rst(self, random_state=None):
        random_state = check_random_state(random_state)
        if self.root is not None:
            root = self.root
        else:
            random_state.randint(0, self.number_of_vertices)

        self.initialize()
        if len(self.edges) != 0:
            raise Exception('Default random init on Tree only accept empty Tree at initialization.\n\
                            Donot add_edge at initialize() or try other random init function.')

        mark = [False] * self.number_of_vertices
        mark[root] = True
        visited_nodes = 1

        v0 = root
        while visited_nodes != self.number_of_vertices:
            v1 = random_state.choice(self.potential_adj[v0])
            if not mark[v1]:
                self.add_edge(v0, v1)
                mark[v1] = True
                visited_nodes += 1
            v0 = v1

        self.repair()

    def from_edge_list(self, edge_list: EdgeList, check_validity: bool = True):
        if any(len(edge) != 2 for edge in edge_list):
            raise ValueError(
                "Each edge has to be a list or tuple containing 2 vertices. \
                For example: for two edges: 1-2, 2-3 --> [(1,2), (2,3)}]")
        self.initialize()
        for u, v in edge_list:
            self.add_edge(u, v)
        self.repair()
        if check_validity:
            return self.check_validity()
        return True

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
        self.adjacency[u].append(v)
        self.adjacency[v].append(u)
        self.edges.append((u, v))
        return True

    def check_validity(self) -> bool:
        __root = self.root if self.root is not None else 0
        __visited = [False] * self.number_of_vertices

        def dfs(u):
            __visited[u] = True
            for v in self.adjacency[u]:
                if not __visited[v]:
                    dfs(v)

        dfs(__root)
        return len(self.edges) == self.number_of_vertices-1 and all(__visited)


class KruskalTree(Tree):
    initialization_methods = ['RandWalkRST', 'PrimRST', 'KruskalRST']

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
        super(KruskalTree, self).add_edge(u, v)
        return True

    def random_init(self, random_state=None):
        if self._initialization_method == 'KruskalRST':
            self.create_kruskal_rst(random_state)
        else:
            super(KruskalTree, self).random_init(random_state)

    def create_kruskal_rst(self, random_state=None):
        """random_init.

        Args:
            random_state:
        """

        random_state = check_random_state(random_state)
        # order = random_state.permutation(np.arange(len(self.potential_edges)))
        weight = random_state.random(len(self.potential_edges))
        order = np.argsort(-weight)
        self.initialize()
        for i in order:
            u, v = self.potential_edges[i]
            if self.try_add_edge(u, v):
                self.add_edge(u, v)

        self.repair()


class RootedTree(Tree):
    initialization_methods = ['RandWalkRST', 'PrimRST']

    def __init__(self, number_of_vertices: int, root: int, potential_edges: EdgeList = None):
        if root is None or root < 0 or root >= number_of_vertices:
            raise ValueError(
                "Invalid root param, requires 0 <= root < number_of_vertices")

        super(RootedTree, self).__init__(number_of_vertices,
                                         root=root, potential_edges=potential_edges)

    def initialize(self):
        super(RootedTree, self).initialize()
        self.parent = [-1] * self.number_of_vertices
        self.depth = [-1] * self.number_of_vertices
        self.parent[self.root] = self.root
        self.depth[self.root] = 0

    def try_add_edge(self, u: int, v: int) -> bool:
        return (self.parent[u] == -1) ^ (self.parent[v] == -1)

    def add_edge(self, u: int, v: int) -> bool:
        if not self.try_add_edge(u, v):
            return False
        if self.parent[u] == -1:
            self.parent[u] = v
            self.depth[u] = self.depth[v] + 1
        else:
            self.parent[v] = u
            self.depth[v] = self.depth[u] + 1
        super(RootedTree, self).add_edge(u, v)
        return True

    def create_prim_rst(self, random_state=None):
        """create_prim_rst.
            This implementation is not good.
            I cannot find any data structure that support both random choice and insert, remove element
            This implementation does not take care unconnected graph (no tree)

        Args:
            random_state:
        """
        random_state = check_random_state(random_state)

        self.initialize()

        # Set of connected nodes
        C = set()
        # eligible edges
        A = rset()

        # Init tree
        for u in range(self.number_of_vertices):
            if self.parent[u] != -1:
                C.add(u)
                for v in self.potential_adj[u]:
                    if v not in C:
                        A.add((u, v))

        while len(C) < self.number_of_vertices:
            u, v = A.random_choice(random_state)
            A.remove((u, v))
            if v not in C:
                self.add_edge(u, v)
                C.add(v)
                for w in self.potential_adj[v]:
                    if w not in C:
                        A.add((v, w))

            if len(A) == 0 and len(C) != self.number_of_vertices:
                raise ValueError('Cannot create random spanning tree from unconnected tree')

        self.repair()

    def create_random_walk_rst(self, random_state=None):
        random_state = check_random_state(random_state)

        self.initialize()
        mark = [False] * self.number_of_vertices
        visited_nodes = 0
        for u in range(self.number_of_vertices):
            if self.parent[u] != -1:
                mark[u] = True
                visited_nodes += 1

        v0 = self.root
        while visited_nodes != self.number_of_vertices:
            v1 = random_state.choice(self.potential_adj[v0])
            if not mark[v1]:
                self.add_edge(v0, v1)
                mark[v1] = True
                visited_nodes += 1
            v0 = v1

        self.repair()

    def sort_by_bfs_order(self, edge_list):
        adj = self.get_adjacency(edge_list)
        __visited = [False] * self.number_of_vertices
        queue = deque()
        edge_list = []
        queue.append(self.root)

        while (len(queue) > 0):
            u = queue.popleft()
            if __visited[u]:
                continue
            __visited[u] = True

            for v in adj[u]:
                if not __visited[v]:
                    edge_list.append((u, v))
                    queue.append(v)

        return edge_list

    def from_edge_list(self, edge_list: EdgeList, check_validity: bool = True):
        edge_list = self.sort_by_bfs_order(edge_list)
        return super(RootedTree, self).from_edge_list(edge_list, check_validity=check_validity)

class LinkCutTree(Tree):
    def initialize(self):
        raise NotImplementedError

    def link(self, u: int, v: int):
        raise NotImplementedError

    def cut(self, u: int, v: int):
        raise NotImplementedError
