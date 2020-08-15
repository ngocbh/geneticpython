"""
# Filename: int_individual.py
# Description:
# Created by ngocjr7 on [11-06-2020 09:19:13]
"""
from __future__ import absolute_import

from geneticpython.core.individual import Individual
from geneticpython.core.individual.chromosome import IntChromosome

class IntIndividual(Individual):

    def __init__(self, length, domains):
        self.chromosome = IntChromosome(length=length, domains=domains)

if __name__ == '__main__':
    pass
