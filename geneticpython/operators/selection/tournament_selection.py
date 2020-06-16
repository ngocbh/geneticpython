"""
# Filename: tournament_selection.py
# Description:
# Created by ngocjr7 on [09-06-2020 22:43:10]
"""
from __future__ import absolute_import

from .selection import Selection
from ...individual import Individual

from typing import List, Union, Callable
from bisect import bisect_right
from itertools import accumulate
from functools import cmp_to_key
from random import Random

import random


class TournamentSelection(Selection):
    """
        choose k (the tournament size) individuals from the population at random
        choose the best individual from the tournament with probability p
        choose the second best individual with probability p*(1-p)
        choose the third best individual with probability p*((1-p)^2)
        and so on
    """
    def __init__(self, tournament_size : int = 2, p : float = 1.0):
        self.tournament_size = tournament_size
        if p <= 0.0 or p > 1.0:
            raise ValueError('Invalid probability 0 <= p <= 1')
        self.p = p

    def single_objective_comparator(self, x : Individual, y: Individual) -> int:
        if x.objective < y.objective:
            return -1
        elif x.objective > y.objective:
            return 1
        else:
            return 0

    def select(self, size: int,
            population: List[Individual], 
            comparator: Callable[[Individual, Individual], bool] = None,
            rand : Random = Random()) -> List[Individual]:
        
        if not comparator:
            comparator = self.single_objective_comparator

        # Check validity of tournament size.
        if self.tournament_size > len(population):
            msg = 'Tournament size({}) is larger than population size({})'
            raise ValueError(msg.format(self.tournament_size, len(population)))
        
        selected_indvs = []
        
        for _ in range(size):
            chosen = None
            competitors = rand.sample(population, self.tournament_size)
            competitors.sort(key=cmp_to_key(comparator))

            for i in range(len(competitors)):
                if rand.uniform(0, 1) <= self.p:
                    chosen = competitors[i]
                    break
            
            if not chosen:
                chosen = competitors[rand.randint(0, len(competitors)-1)]
            
            selected_indvs.append(chosen)
        
        return selected_indvs

            

    
if __name__ == '__main__':
    pass