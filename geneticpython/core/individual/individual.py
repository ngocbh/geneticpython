"""
# Problem: individual.py
# Description: 
# Created by ngocjr7 on [2020-03-29 18:39:05]
"""
from __future__ import absolute_import

from .solution import Solution
from .chromosome import Chromosome, IntChromosome
from geneticpython.utils.validation import check_random_state

from typing import List, Union, Callable, Tuple, NewType
from copy import deepcopy

import numpy as np
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

    def __init__(self, chromosome: Chromosome, solution: Solution = None):
        """
            Initialization for Individual
            :init chromosome
        """
        self.chromosome = chromosome
        self.solution = solution
        self._objective = None
        self._coefficient = None
        self._objectives = None
        self._coefficients = None
        self.random_state = None

    def __str__(self):
        if self._objective:
            return str(self.chromosome) + ' -> ' + str(self.objective) + '\n'
        else:
            return str(self.chromosome) + ' -> ' + str(self.objectives) + '\n'

    def __repr__(self):
        if self._objective:
            return str(self.chromosome) + ' -> ' + str(self.objective) + '\n'
        else:
            return str(self.chromosome) + ' -> ' + str(self.objectives) + '\n'

    def set_random_state(self, random_state):
        self.random_state = random_state

    def clone(self):
        """
            Clone a new individual from current one.
        """
        indiv = deepcopy(self)
        return indiv

    def init(self, chromosome: Chromosome = None, solution: Solution = None, random_state=None):
        if chromosome != None:
            self.chromosome = chromosome
        elif solution != None:
            self.solution = solution
            self.chromosome = self.encode(solution)
        else:
            # initialize randomly
            self.random_init(random_state=random_state)

    def random_init(self, random_state=None):
        random_state = check_random_state(random_state or self.random_state)
        self.chromosome.init_genes(random_state=random_state)

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

    def encode(self, solution : Solution):
        """
            Encode from solution to chromosome

        :return: The chromsome sequence
        :rtype: list of something
        """
        raise NotImplementedError


if __name__ == "__main__":
    pass

