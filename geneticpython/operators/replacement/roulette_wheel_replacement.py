"""
# Filename: roulette_wheel_replacement.py
# Description:
# Created by ngocjr7 on [07-06-2020 00:54:08]
"""
from __future__ import absolute_import

from typing import List, Union

from .replacement import Replacement
from ...individual import Individual
from ...operators import RouletteWheelSelection

from random import Random

class RouletteWheelReplacement(Replacement):

    def replace(self, size : int, population: List[Individual], 
            offspring_population: List[Individual],
            rand: Random = Random()) -> List[Individual]:

        selection = RouletteWheelSelection()
        best_indv = min(population, key=lambda indv: indv.objective)

        population.extend(offspring_population)
        
        new_population = selection.select(size-1, population, rand=rand, is_unique=True)
        new_population.append(best_indv)

        return new_population