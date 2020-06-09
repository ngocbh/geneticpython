"""
# Problem: geneticengine.py
# Description: 
# Created by ngocjr7 on [2020-03-29 22:58:36]
"""
from __future__ import absolute_import

from functools import wraps
from typing import List, Union, Callable
from tqdm.auto import tqdm

from .individual import Individual
from .population import Population
from .operators import Selection, Crossover, Mutation, Replacement

import random
import math


class GAEngine:
    rand = None

    def __init__(self, population: Population, 
            selection : Selection = None, 
            crossover : Crossover = None, 
            mutation : Mutation = None, 
            replacement : Replacement = None, 
            objective : Callable[[Individual], Union[float,int]] = None,
            selection_size : int = None,
            random_state : int = None, 
            max_iter=100):
            
        self.population = population
        self.MAX_ITER = max_iter 
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.replacement = replacement
        self.objective = objective

        if not selection_size:
            self.selection_size = self.population.size

        if random_state:
            self.rand = random.Random(random_state)
        else:
            self.rand = random.Random()
    
    def create_seed(self, seed : int):
        self.rand = random.Random(seed)

    def set_selection(self, selection : Selection):
        self.selection = selection
    
    def set_crossover(self, crossover : Crossover):
        self.crossover = crossover
    
    def set_mutation(self, mutation : Mutation):
        self.mutation = mutation

    def set_replacement(self, replacement : Replacement):
        self.replacement = replacement
    
    def reproduction(self, mating_population : List[Individual]) -> List[Individual]:
        childs = []
        for i in range(0,len(mating_population), 2):
            childs_temp = self.crossover.cross(father=mating_population[i], mother=mating_population[i+1], rand=self.rand)
            childs.extend(childs_temp)

        for child in childs:
            child = self.mutation.mutate(child, rand=self.rand)
        
        return childs

    def evaluate(self, population: List[Individual]) -> List[Individual]:
        ret = list()
        for indv in population:
            indv.objective = self.objective(indv)
            ret.append(indv)
        return ret

    def get_best_indv(self) -> Individual:
        best_indv = min(self.population.individuals, key= lambda indv: indv.objective)
        return best_indv.clone()

    def run(self):
        self.population.individuals = self.population.init_population(self.rand)
        self.evaluate(self.population.individuals)

        pbar = tqdm(range(self.MAX_ITER))
        for g in pbar:
            mating_population = self.selection.select(self.selection_size,
                                                self.population,
                                                rand=self.rand)
            
            offspring_population = self.reproduction(mating_population)
            offspring_population = self.evaluate(offspring_population)

            self.population.individuals = self.replacement.replace(
                                            self.population.size,
                                            self.population.individuals, 
                                            offspring_population,
                                            rand=self.rand)

            best_indv = self.get_best_indv()
            pbar.set_description(f'best objective {best_indv.objective:.6f}')
            
    def register_objective(self, fn):
        """
            register objective function
        """
        @wraps(fn)
        def _fn_with_objective_check(indv):
            '''
            A wrapper function for objective function with objective value check.
            '''
            # Check indv type.
            if not isinstance(indv, Individual):
                raise TypeError('indv\'s class must be subclass of IndividualBase')

            # Check objective.
            objective = fn(indv)
            is_invalid = not isinstance(objective,(float, int)) or (math.isnan(objective))
            if is_invalid:
                msg = 'objective value(value: {}, type: {}) is invalid'
                msg = msg.format(objective, type(objective))
                raise ValueError(msg)
            return objective
        
        self.objective = _fn_with_objective_check

    def maximize(self, fn):
        ''' A decorator for maximizing the objective function.
        :param fn: Original objective function
        :type fn: function
        '''
        @wraps(fn)
        def _maximize(indv):
            return -fn(indv)

        return _maximize
    

if __name__ == "__main__":
    pass