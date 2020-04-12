"""
# Problem: binary_individual.py
# Description: 
# Created by ngocjr7 on [2020-03-29 22:37:50]
"""
from __future__ import absolute_import

from .individual import Individual
from .chromosome import Chromosome
from .solution import Solution
from .gene import Gene

class BinaryIndividual(Individual):
    """
        BinaryIndividual only accept gene with binary value
    """
    def __init__(self, length):
        self.chromosome = Chromosome(length, [(0,1)])
        self.solution = Solution()
        self.fitness = None