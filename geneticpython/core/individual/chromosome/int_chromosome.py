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
    def __init__(self, length: int, domains: [list, tuple]):
        super(IntChromosome, self).__init__(length, domains, 'int32')

    @property
    def is_valid(self):
        pass

    def init_genes(self, genes=None, rand=random.Random()):
        if genes != None:
            if (isinstance(genes,(tuple,list)) and len(genes) != self.length):
                self.genes = np.array(genes)
            elif isinstance(genes, np.ndarray) and genes.ndim == 1 and genes.shape[0] == self.length:
                self.genes = genes
            else:
                raise Exception("genes has to be an instance of tuple or list and has the same length as chromosome")
        else:   
            self.genes = np.array([
                    rand.randint(int(self.lower_bound[i]), int(self.upper_bound[i])) for i in range(self.length)
                ])
        

        