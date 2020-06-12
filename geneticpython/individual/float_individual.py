"""
# Filename: float_individual.py
# Description:
# Created by ngocjr7 on [11-06-2020 09:16:17]
"""
from __future__ import absolute_import

from .chromosome import FloatChromosome
from .individual import Individual

class FloatIndividual(Individual):

    def __init__(self, length, domain):
        self.chromosome = FloatChromosome(length, domain)
        self.objective = None
        self.objectives = None
        
if __name__ == '__main__':
    pass