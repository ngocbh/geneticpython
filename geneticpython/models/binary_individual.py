"""
# Problem: binary_individual.py
# Description: 
# Created by ngocjr7 on [2020-03-29 22:37:50]
"""
from __future__ import absolute_import

from geneticpython.core.individual import Individual
from geneticpython.core.individual.chromosome import IntChromosome

import numpy as np

class BinaryIndividual(Individual):
    """
        BinaryIndividual only accept gene with binary value
    """

    def __init__(self, length):
        chromosome = IntChromosome(length, [0, 1])
        super(BinaryIndividual, self).__init__(chromosome)

    def decode(self):
        return np.copy(self.chromosome.genes)
