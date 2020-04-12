"""
# Problem: geneticengine.py
# Description: 
# Created by ngocjr7 on [2020-03-29 22:58:36]
"""
from __future__ import absolute_import

from functools import wraps
from .individual import Individual

import random
import math

class GeneticEngine:
    rand = None

    def __init__(self, population, selection=None, crossover=None, mutation=None, max_iter=100):
        self.population = population
        self.rand = random.Random()
        self.MAX_ITER = max_iter 
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.selection_size = 100
    
    def create_seed(self, seed):
        self.rand = random.Random(seed)

    def set_selection(self, selection):
        self.selection = selection
    
    def set_crossover(self, crossover):
        self.crossover = crossover
    
    def set_mutation(self, mutation):
        self.mutation = mutation
    
    def assign_population_fitness(self):
        if not self.fitness:
            raise Exception('You have to provide fitness function to GeneticEngine by decolator @engine.register_fitness')
        self.population.all_fits(self.fitness)

    def register_fitness(self, fn):
        """
            register fitness function
        """
        @wraps(fn)
        def _fn_with_fitness_check(indv):
            '''
            A wrapper function for fitness function with fitness value check.
            '''
            # Check indv type.
            if not isinstance(indv, Individual):
                raise TypeError('indv\'s class must be subclass of IndividualBase')

            # Check fitness.
            fitness = fn(indv)
            is_invalid = not isinstance(fitness,(float, int)) or (math.isnan(fitness))
            if is_invalid:
                msg = 'Fitness value(value: {}, type: {}) is invalid'
                msg = msg.format(fitness, type(fitness))
                raise ValueError(msg)
            return fitness
        
        self.fitness = _fn_with_fitness_check
    
    def run(self):
        self.cur_generation = 0
        if self.population.init_population == None:
            raise Exception('Population initialization hasnot implemented yet')
        self.population.init_population(self.rand)
        self.assign_population_fitness()
        for g in range(self.MAX_ITER):
            parents = self.selection.select(self.selection_size,self.population,fitness_func=self.fitness, rand=self.rand)
            childs = []
            for i in range(0,len(parents), 2):
                childs_temp = self.crossover.cross(father=parents[i], mother=parents[i+1], rand=self.rand)
                childs.extend(childs_temp)
            # print(childs)
            for child in childs:
                child = self.mutation.mutate(child, rand=self.rand)
            # print(childs)

            best_indv = self.population.get_best_indv(self.fitness)
            self.population.individuals.extend(childs)
            slt_indvs = self.selection.select(self.population.size-1,self.population, fitness_func=self.fitness, rand=self.rand)
            slt_indvs.append(best_indv)
            self.population.individuals = slt_indvs

if __name__ == "__main__":
    pass