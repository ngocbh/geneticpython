"""
# Problem: population.py
# Description: 
# Created by ngocjr7 on [2020-03-29 23:29:36]
"""
from __future__ import absolute_import

from functools import wraps
from typing import List, Union, Callable
from tqdm.auto import tqdm


from .individual import Individual
from random import Random
import random

class Population():

    def __init__(self, individual_temp: Individual, size=100, init_population : Callable[[], List[Individual]] = None):
        self.individual_temp = individual_temp
        self.rand = random.Random()
        self.size = size
        if init_population:
            self.init_population = init_population
        else:
            self.init_population = self.init_population_randomly
        self.individuals = []

    def __str__(self):
        ret = '[Begin population\n'
        for indiv in self.individuals:
            ret += str(indiv) + '\n'
        ret += 'End population]'
        return ret
    
    def __repr__(self):
        ret = '['
        for indiv in self.individuals:
            ret += str(indiv) + '\n'
        ret += ']'
        return ret
    
    def __getitem__(self, key):
        '''
        Get individual by index.
        '''
        if key < 0 or key >= len(self.individuals):
            raise IndexError('Individual index({}) out of range'.format(key))
        return self.individuals[key]

    def __len__(self):
        '''
        Get length of population.
        '''
        return len(self.individuals)

    def create_seed(self, seed):
        self.rand = random.Random(seed)
    
    def set_rand(self,rand):
        self.rand = rand

    def set_initialization(self, callback : Callable[[], List[Individual]]):
        self.init_population = callback

    def init_population_randomly(self, rand : Random = Random()) -> List[Individual]:
        ret = []
        for _ in range(self.size):
            new_indiv = self.individual_temp.clone()
            new_indiv.init(rand=rand)
            ret.append(new_indiv)
        return ret

    def clear(self):
        self.individuals.clear()

    def sort(self,reversed=True):
        self.individuals.sort(key=lambda x: x.objective,reversed=reversed)
    
    def all_fits(self):
        return [indv.objective for indv in self.individuals]

    