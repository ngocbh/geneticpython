"""
# Problem: individual.py
# Description: 
# Created by ngocjr7 on [2020-03-29 18:39:05]
"""
from __future__ import absolute_import

from .solution import Solution
from .chromosome import Chromosome, IntChromosome

from typing import Union

from copy import deepcopy
from random import Random

import numpy as np
import random
import inspect


class Individual:
    """
        Representation of an Individual.
        :chromosome always is a list of something.
        :solution is instance of Solution
        :gene_domains is range of each gene in chromosome,
        and gene_domains has the same length as chromosome,
        if not, gene_domains will extend the last gene domain to the rest. 
    """

    def __init__(self, chromosome: Chromosome, solution: Solution = None, rand: Random = Random()):
        """
            Initialization for Individual
            :init chromosome
        """
        self.chromosome = chromosome
        self.solution = solution
        self.rand = rand
        self._objective = None
        self._coefficient = None
        self._objectives = None
        self._coefficients = None

    def __str__(self):
        if self._objective:
            return str(self.chromosome) + ' -> ' + str(self._objective) + '\n'
        else:
            return str(self.chromosome) + ' -> ' + str(self._objectives) + '\n'

    def __repr__(self):
        if self._objective:
            return str(self.chromosome) + ' -> ' + str(self._objective) + '\n'
        else:
            return str(self.chromosome) + ' -> ' + str(self._objectives) + '\n'

    def create_seed(self, seed):
        self.rand = random.Random(seed)

    def set_rand(self, rand):
        self.rand = rand

    def clone(self):
        """
            Clone a new individual from current one.
        """
        indiv = deepcopy(self)
        return indiv

    def init(self, chromosome: Chromosome = None, solution: Solution = None, rand=random.Random()):
        if chromosome != None:
            self.chromosome = chromosome
        elif solution != None:
            self.solution = solution
            self.chromosome = self.encode(solution)
        else:
            # initialize randomly
            self.chromosome.init_genes(rand=rand)

    def update_genes(self, genes: Union[np.ndarray, tuple, list]):
        self.chromosome.init_genes(genes=genes)

    @property
    def objective(self):
        return self._objective * self._coefficient

    @property
    def objectives(self):
        objectives = []
        for _coefficient, _objective in zip(self._coefficients, self._objectives):
            objectives.append(_coefficient * _objective)

        return objectives

    def is_valid(self):
        return self.chromosome.is_valid() and (not self.solution or self.solution.is_valid())

    def decode(self):
        """
            Decode chromosome sequence to readable solution

        :return solution
        :rtype Solution
        """
        raise NotImplementedError

    def encode(self, solution):
        """
            Encode from solution to chromosome

        :return: The chromsome sequence
        :rtype: list of something
        """
        raise NotImplementedError


if __name__ == "__main__":
    pass
