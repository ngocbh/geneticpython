"""
# Problem: chromosome.py
# Description: 
# Created by ngocjr7 on [2020-03-29 22:10:24]
"""
from __future__ import absolute_import

import numpy as np

import random

class Chromosome():
    def __init__(self, length: int, domain: [list, tuple]):
        if not isinstance(domain,(list,tuple)) and len(domain) == 2:
            raise Exception('domain has to be instance of list or tuple \
                and contains exactly 2 numbers')

        self.length = length
        self.max_value, self.min_value = domain
        self.genes = np.empty(length)
    
    def __str__(self):
        return str(self.genes)

    def __repr__(self):
        return str(self.genes)
    
    def __getitem__(self, key):
        '''
        Get individual by index.
        '''
        if key < 0 or key >= self.length:
            raise IndexError('Individual index({}) out of range'.format(key))
        return self.genes[key]

    def __setitem__(self, key, value):
        '''
        Get individual by index.
        '''
        if key < 0 or key >= self.length:
            raise IndexError('Individual index({}) out of range'.format(key))
        self.genes[key] = value

    def __len__(self):
        '''
        Get length of population.
        '''
        return len(self.genes)

    def suffix(self, i):
        return self.genes[i:]
    
    def prefix(self, i):
        return self.genes[:i]

    @property
    def is_valid(self):
        for gene in self.genes:
            if not gene.is_valid:
                return False
        return True

    def init_genes(self, genes=None, rand=None):
        raise NotImplementedError
        

        