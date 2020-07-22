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
        chromosome = FloatChromosome(length, domain)
        super(FloatIndividual, self).__init__(chromosome)


if __name__ == '__main__':
    pass

