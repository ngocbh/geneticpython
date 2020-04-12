"""
# Problem: individual.py
# Description: 
# Created by ngocjr7 on [2020-03-29 18:39:05]
"""
from __future__ import absolute_import

from .solution import Solution
from .chromosome import Chromosome

from copy import deepcopy

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
    rand = None

    def __init__(self, chromosome, solution=None):
        """
            Initialization for Individual
            :init chromosome
        """
        if not isinstance(chromosome,Chromosome):
            raise Exception('chromosome has to be instance of Chromosome')

        self.chromosome = chromosome
        self.solution = solution
        self.rand = random.Random()
        self.fitness = None

    def __str__(self):
        return str(self.chromosome) + ' -> ' + str(self.fitness)

    def __repr__(self):
        return str(self.chromosome)  + '->' + str(self.fitness)

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

    def init(self, chromosome=None, solution=None, rand=None):
        if chromosome != None:
            if not isinstance(chromosome, Chromosome):
                raise Exception('chromosome is not instance of Chromosome')
            self.chromosome = chromosome
        elif solution != None:
            if not isinstance(solution, Solution):
                raise Exception('solution is not instance of Solution')
            self.solution = solution
            self.chromosome = self.encode(solution)
        else:
            # initialize randomly
            if not rand:
                rand = random.Random()
            
            self.chromosome.init_genes(rand=rand)
    
    def is_valid(self):
        return self.chromosome.is_valid() & self.solution.is_valid()

    def decode(self):
        """
            Decode chromosome sequence to readable solution
        
        :return solution
        :rtype Solution
        """
        raise NotImplementedError

    def encode(self):
        """
            Encode from solution to chromosome

        :return: The chromsome sequence
        :rtype: list of something
        """
        raise NotImplementedError
    
    def fitness(self):
        """
            fitness function is used to evaluate solution

        :return: The chromsome sequence
        :rtype: list of something
        """
        raise NotImplementedError

if __name__ == "__main__":
    pass