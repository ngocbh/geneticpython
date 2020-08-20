"""
# Problem: chromosome.py
# Description: 
# Created by ngocjr7 on [2020-03-29 22:10:24]
"""
from __future__ import absolute_import

from typing import List, Union, Callable, Dict, Tuple

import numpy as np
import random
import copy

class Chromosome():
    def __init__(self, length: int, domains: Union[List, Tuple], dtype: str = 'float32'):
        self.lower_bound, self.upper_bound = Chromosome._formated_domains(length, domains)
        self.length = length
        self.genes = np.empty(length, dtype=dtype)
    
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

    @staticmethod
    def _formated_domains(length, domains):
        if isinstance(domains,(list,tuple)) and len(domains) == 2 and \
                all(isinstance(value, (float, int)) for value in domains):
            return np.array([domains[0] for _ in range(length)]), np.array([domains[1] for _ in range(length)])
        elif isinstance(domains, (list, tuple)) and len(domains) == length and\
                all(isinstance(domain, (list, tuple)) for domain in domains) and\
                all((len(domain) == 2) for domain in domains) and \
                all(isinstance(value, (float, int)) for domain in domains for value in domain) and\
                all((domain[0] < domain[1]) for domain in domains):
            return np.array([domain[0] for domain in domains]), np.array([domain[1] for domain in domains])
        else:
            raise ValueError('There are two types of accepted domains\n\
                (min_value, max_value): this domain will be applied for all variable\n\
                [(min_value_1, max_value_1),... (min_value_length, max_value_length)]: \n\
                each will be applied for a variable respectively')

    @property
    def is_valid(self):
        pass

    def init_genes(self, genes=None, random_state=None):
        raise NotImplementedError
        

        
