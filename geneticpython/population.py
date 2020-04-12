"""
# Problem: population.py
# Description: 
# Created by ngocjr7 on [2020-03-29 23:29:36]
"""
from __future__ import absolute_import

import random

class Population:

    def __init__(self, individual_temp, size=100):
        self.individual_temp = individual_temp
        self.rand = random.Random()
        self.size = size
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

    def set_initialization(self, callback):
        self.init_population = callback

    def init_population_randomly(self, rand=None):
        if not rand:
            rand = random.Random()

        for _ in range(self.size):
            new_indiv = self.individual_temp.clone()
            new_indiv.init(rand=rand)
            self.individuals.append(new_indiv)

    def clear(self):
        self.individuals.clear()

    def sort(self,reversed=True):
        self.individuals.sort(key=lambda x: x.fitness,reversed=reversed)
    
    def all_fits(self, fitness_func):
        fits = []
        for indv in self.individuals:
            indv.fitness = fitness_func(indv)
            fits.append(indv.fitness)
        return fits

    def get_best_indv(self, fitness_func):
        best_indv = None
        best_fit = -9223372036854775807
        for indv in self.individuals:
            indv.fitness = fitness_func(indv)
            if indv.fitness > best_fit:
                best_fit = indv.fitness
                best_indv = indv
        return best_indv.clone()
    