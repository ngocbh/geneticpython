"""
# Filename: nsgaiiengine.py
# Description:
# Created by ngocjr7 on [09-06-2020 16:05:40]
"""
from __future__ import absolute_import

from functools import wraps
from typing import List, Union
from random import Random

from .individual import Individual
from .gaengine import GAEngine
import random
import math

def compare(adam : Individual, eva : Individual) -> bool:
    pass

class NSGAIIEngine(GAEngine):
    
    def __init__(self, population: Population, 
            crossover : Crossover = None, 
            mutation : Mutation = None,  
            objectives : List[Callable[[Individual], Union[float,int]]] = None,
            selection_size : int = None,
            random_state : int = None, 
            max_iter=100):
        
        self.population = population
        self.crossover = crossover
        self.mutation = mutation
        self.objectives = objectives
        self.random_state = random_state
        self.max_iter = max_iter

        if not selection_size:
            self.selection_size = self.population.size

        if random_state:
            self.rand = random.Random(random_state)
        else:
            self.rand = random.Random()

    def set_replacement(self, *arg, **kargv):
        raise NotImplementedError('setting replacement is not available in NASGAII.\
            Use Non dominated sorting algorithm by default')

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
            indv.objectives = list()

            for objective in self.objectives:
                indv.objectives.append(objective(indv))

            ret.append(indv)
        return ret

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
        
        if not self.objectives:
            self.objectives = list(_fn_with_objective_check)
        else:
            self.objectives.append(_fn_with_objective_check)

if __name__ == '__main__':
    pass