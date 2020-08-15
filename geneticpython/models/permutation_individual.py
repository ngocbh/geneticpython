
"""
# Filename: permutation_individual.py
# Description:
# Created by ngocjr7 on [11-06-2020 09:19:13]
"""
from __future__ import absolute_import

from geneticpython.core.individual import Individual
from geneticpython.core.individual.chromosome import IntChromosome

class PermutationIndividual(Individual):

    def __init__(self, length, start=1):
        domains = [start, start + length - 1]
        self.start = start
        self.chromosome = IntChromosome(length=length, domains=domains)

    def is_valid(self):
        exists = [0] * self.chromosome.length
        for gene in self.chromosome:
            exists[gene - self.start] = 1
        return all(e == 1 for e in exists)

if __name__ == '__main__':
    pass
