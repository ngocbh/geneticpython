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

import math


class RouletteWheelReplacement(Replacement):
    __EPS = 1e-14

    def replace(self, size: int, population: List[Individual],
                random_state=None) -> List[Individual]:
        selection = RouletteWheelSelection()
        best_indv = min(population, key=lambda indv: indv._objective)

        bad_pop = list()
        for indv in population:
            if not abs(indv._objective - best_indv._objective) < self.__EPS:
                bad_pop.append(indv)

        new_population = [best_indv]
        new_population.extend(selection.select(
            size-1, bad_pop, random_state=random_state, is_unique=True))

        return new_population

