"""
# Problem: chromosome.py
# Description: 
# Created by ngocjr7 on [2020-03-29 22:10:24]
"""
from __future__ import absolute_import

from .gene import Gene

import random

class Chromosome():
    def __init__(self, length, domains):
        self.length = length
        if not isinstance(domains,(list,tuple)):
            raise Exception('domains has to be instance of list or tuple')
        if not isinstance(domains[0],(list,tuple)) or len(domains[0]) != 2:
            raise Exception('domains has to contain a list which contain two number is min_value and max_value respectively')

        while len(domains) < length:
            domains.append(domains[-1])
        domains = domains[:length]

        self.genes = []
        for domain in domains:
            self.genes.append(Gene(domain[0],domain[1]))
    
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
        if genes:
            if not isinstance(genes,(tuple,list)) or len(genes) != self.length:
                raise Exception("genes has to be an instance of tuple or list and has the same length as chromosome")

            for i in range(length):
                self.genes[i].value = genes[i]
        else:        
            if not rand:
                rand = random.Random()
            
            for i in range(self.length):
                self.genes[i].set_random_value(rand)
        

        