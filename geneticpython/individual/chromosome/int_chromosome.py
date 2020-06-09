"""
# Problem: int_chromosome.py
# Description: 
# Created by ngocjr7 on [2020-03-29 22:10:24]
"""
from __future__ import absolute_import

from .chromosome import Chromosome

import numpy as np

import random

class IntChromosome(Chromosome):
    def __init__(self, length: int, domain: [list, tuple]):
        if not isinstance(domain,(list,tuple)) and len(domain) == 2:
            raise Exception('domain has to be instance of list or tuple \
                and contains exactly 2 numbers')

        self.length = length
        self.min_value, self.max_value = domain
        self.genes = np.zeros(length, dtype='int32')
    @property
    def is_valid(self):
        pass

    def init_genes(self, genes=None, rand=random.Random()):
        if genes:
            if not isinstance(genes,(tuple,list)) or len(genes) != self.length:
                raise Exception("genes has to be an instance of tuple or list and has the same length as chromosome")

            self.genes = np.array(genes)
        else:                    
            random_func = lambda x: rand.randint(self.min_value, self.max_value)
            self.genes = np.vectorize(random_func)(self.genes)
        

        