"""
# Filename: network_random_key.py
# Description:
# Created by ngocjr7 on [08-06-2020 14:08:36]
"""
from __future__ import absolute_import

from .individual import Individual
from .chromosome import FloatChromosome

class NetworkRandomKey(Individual):
    """
    """
    def __init__(self, length):
        self.chromosome = FloatChromosome(length, [0,1])
        self.objective = None
        self.objectives = None
    


if __name__ == '__main__':
    pass