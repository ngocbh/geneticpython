"""
# Filename: network_random_key.py
# Description:
# Created by ngocjr7 on [08-06-2020 14:08:36]
"""
from __future__ import absolute_import

from geneticpython.core.individual import Individual, Solution
from geneticpython.core.individual.chromosome import FloatChromosome
from typing import Dict, List, NewType, Tuple, Union

from .tree import KruskalTree, EdgeList

import numpy as np



class NetworkRandomKeys(Individual):
    """
        this code implements Network Random Keys,
        Rothlauf, Franz & Goldberg, David & Heinzl, Armin. (2002). 
        Network Random Keys—A Tree Representation Scheme for Genetic and Evolutionary Algorithms. 
        Evolutionary computation. 10. 75-97. 10.1162/106365602317301781. 
    """

    def __init__(self, number_of_vertices: int, 
                 potential_edges: EdgeList, 
                 chromosome: FloatChromosome = None, 
                 network: KruskalTree = None, 
                 use_encode=False):
        self.network = network or KruskalTree(number_of_vertices, potential_edges=potential_edges)
        edges_size = len(potential_edges)
        chromosome = chromosome or FloatChromosome(edges_size, [0, 1])
        self.number_of_vertices = number_of_vertices
        self.use_encode = use_encode
        self.potential_edges = potential_edges
        if use_encode:
            self.edge_dict = dict()
            idx = 0
            for u, v in potential_edges:
                self.edge_dict[(u, v)] = idx
                self.edge_dict[(v, u)] = idx
                idx += 1
        else:
            self.edge_dict = None

        super(NetworkRandomKeys, self).__init__(chromosome)

    def decode(self) -> KruskalTree:
        genes = np.copy(self.chromosome.genes)
        order = np.argsort(-genes)

        self.network.initialize()

        for i in order:
            u, v = self.potential_edges[i]
            self.network.add_edge(u, v)

        self.network.repair()
        return self.network
    
    def encode(self, network: KruskalTree):
        if not self.use_encode:
            raise NotImplementedError("You can init with use_encode to force use bias encoding method")

        order = []
        used = [False] * self.chromosome.length
        for u, v in network.edges:
            idx = self.edge_dict[(u, v)]
            order.append(idx)
            used[idx] = True

        for i, b in enumerate(used):
            if not b:
                order.append(i)

        n = len(order) + 2
        step = 1.0/n
        genes = np.zeros(self.chromosome.length)
        for i, e in enumerate(order):
            genes[e] = 1 - step * (i+1)
            
        self.update_genes(genes)
        self.network = network

if __name__ == '__main__':
    pass
