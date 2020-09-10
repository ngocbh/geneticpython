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

    def __init__(self, number_of_vertices: int, edge_list: EdgeList, network: KruskalTree = None):
        self.network = network or KruskalTree(number_of_vertices, edge_list=edge_list)
        edges_size = len(self.network.edge_list)
        chromosome = FloatChromosome(edges_size, [0, 1])
        super(NetworkRandomKeys, self).__init__(chromosome)

    def decode(self) -> KruskalTree:
        genes = np.copy(self.chromosome.genes)
        order = np.argsort(-genes)

        self.network.initialize()

        for i in order:
            u, v = self.network.edge_list[i]
            self.network.add_edge(u, v)

        self.network.repair()
        return self.network
    
    @classmethod
    def encode(cls, solution : Solution):
        raise NotImplementedError("NetworkRandomKeys does not support encoding method")

if __name__ == '__main__':
    pass
