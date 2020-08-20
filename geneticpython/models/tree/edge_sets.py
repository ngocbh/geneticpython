"""
File: edges_set.py
Created by ngocjr7 on 2020-08-16 23:10
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""
from __future__ import absolute_import

from geneticpython.core.individual import Individual, IntChromosome
from geneticpython.models.tree.tree import Tree

class EdgeSets(Individual):
    def __init__(self, number_of_vertices, start=1):
        self.number_of_vertices = number_of_vertices
        self.start = start
        chromosome = IntChromosome(
            2*number_of_vertices-2, domains=[start, start + number_of_vertices - 1])
        super(EdgeSets, self).__init__(chromosome=chromosome)

    def decode(self) -> Tree:
        raise NotImplementedError

    @classmethod
    def encode(cls, tree : Tree):
        raise NotImplementedError
