"""
# Filename: network_random_key.py
# Description:
# Created by ngocjr7 on [08-06-2020 14:08:36]
"""
from __future__ import absolute_import

from .individual import Individual
from .chromosome import FloatChromosome
from typing import Dict, List

import numpy as np


class Network():

    def __init__(self):
        pass

    def init_solution(self):
        raise NotImplementedError

    def try_add_edge(self, i: int):
        raise NotImplementedError

    def add_edge(self, i: int):
        raise NotImplementedError

    def repair(self):
        pass


class NetworkRandomKeys(Individual):
    """
        this code implements Network Random Keys,
        Rothlauf, Franz & Goldberg, David & Heinzl, Armin. (2002). 
        Network Random Keys—A Tree Representation Scheme for Genetic and Evolutionary Algorithms. 
        Evolutionary computation. 10. 75-97. 10.1162/106365602317301781. 
    """

    def __init__(self, length, network: Network):
        chromosome = FloatChromosome(length, [0, 1])
        super(NetworkRandomKeys, self).__init__(chromosome)
        self.network = network

    def decode(self):
        genes = np.copy(self.chromosome.genes)
        order = np.argsort(-genes)

        self.network.init_solution()

        for i in order:
            if self.network.try_add_edge(i):
                self.network.add_edge(i)

        self.network.repair()
        return self.network


if __name__ == '__main__':
    pass

