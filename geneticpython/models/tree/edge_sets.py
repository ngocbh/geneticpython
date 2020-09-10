"""
File: edges_set.py
Created by ngocjr7 on 2020-08-16 23:10
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""
from __future__ import absolute_import

from geneticpython.core.individual import Individual, IntChromosome
from geneticpython.models.tree.tree import Tree, KruskalTree, EdgeList, RootedTree
from geneticpython.utils.validation import check_random_state
from typing import Set, Tuple, List

import numpy as np


class EdgeSets(Individual):
    def __init__(self, number_of_vertices, 
                 solution: Tree = None,
                 edge_list: EdgeList = None):
        self.number_of_vertices = number_of_vertices
        chromosome = IntChromosome(
            (self.number_of_vertices-1) * 2, domains=[0, number_of_vertices - 1])
        super(EdgeSets, self).__init__(chromosome=chromosome)
        self.solution = solution or Tree(number_of_vertices, edge_list=edge_list)
        self.__initialization_method = 'KruskalRST'

    def set_initialization_method(self, method: str):
        if method not in Tree.initialization_methods:
            raise ValueError(f"Invalid initialization method, only accept {Tree.initialization_methods}")
        self.__initialization_method = method

    def decode(self) -> Tree:
        """decode.

        Args:

        Returns:
            Tree:
        """
        self.solution.initialize()
        _is_valid = True
        for i in range(0, self.chromosome.length, 2):
            u, v = self.chromosome[i], self.chromosome[i+1]
            _is_valid &= self.solution.add_edge(u, v)

        self.solution._is_valid = _is_valid
        self.solution.repair()
        return self.solution

    def encode(self, solution: Tree, random_state=None):
        """encode.

        Args:
            solution (Tree): solution
            random_state:
        """
        order = [i for i in range(solution.number_of_vertices-1)]

        genes = [0] * self.chromosome.length
        edge_list = list(solution.edges)
        for i, j in enumerate(order):
            genes[2*i], genes[2*i+1] = edge_list[j]

        self.update_genes(genes)

    def random_init(self, random_state=None):
        """random_init.

        Args:
            random_state:
        """
        if self.__initialization_method == 'KruskalRST':
            self.solution.create_kruskal_rst(random_state)

        genes = []
        for edge in self.solution.edges:
            genes.extend(edge)
        self.update_genes(genes)
