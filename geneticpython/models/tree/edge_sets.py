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
from copy import deepcopy

import numpy as np


class EdgeSets(Individual):
    """EdgeSets.
    """

    def __init__(self, number_of_vertices, 
                 chromosome : IntChromosome = None,
                 solution: Tree = None,
                 potential_edges: EdgeList = None,
                 init_method: str = None):
        self.number_of_vertices = number_of_vertices
        chromosome = chromosome or IntChromosome(
            (self.number_of_vertices-1) * 2, domains=[0, number_of_vertices - 1])
        super(EdgeSets, self).__init__(chromosome=chromosome)
        self.solution = solution or Tree(number_of_vertices, potential_edges=potential_edges, init_method=init_method)
        if init_method is not None:
            self.solution.set_initialization_method(init_method)

    def clone(self):
        number_of_vertices = self.number_of_vertices
        solution = self.solution.clone()
        chromosome = deepcopy(self.chromosome)

        return EdgeSets(number_of_vertices, chromosome=chromosome, solution=solution)

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
        self.solution = solution

    def random_init(self, random_state=None):
        """random_init.

        Args:
            random_state:
        """
        self.solution.random_init(random_state)
        genes = []
        for edge in self.solution.edges:
            genes.extend(edge)
        self.update_genes(genes)
