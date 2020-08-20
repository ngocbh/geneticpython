"""
# Problem: roulette_wheel_selection.py
# Description: 
# Created by ngocjr7 on [2020-03-31 14:55:40]
"""
from __future__ import absolute_import

from .selection import Selection
from ...individual import Individual
from geneticpython.utils.validation import check_random_state

from typing import List, Union
from bisect import bisect_right
from itertools import accumulate


class RouletteWheelSelection(Selection):
    def __init__(self):
        pass

    def select(self, size: int,
               population: List[Individual],
               is_unique=False,
               random_state=None) -> List[Individual]:
        random_state = check_random_state(random_state)
        fits = [float(indv._objective) for indv in population]
        max_fit = max(fits)
        fits = [(max_fit - e_fit + 1) for e_fit in fits]
        sum_fit = sum(fits)
        wheel = list(accumulate([i/sum_fit for i in fits]))

        selected = [True] * len(population)

        selected_indvs = []

        for _ in range(size):
            idx = bisect_right(wheel, random_state.random())
            while is_unique and not selected[idx] and idx > -len(selected):
                idx -= 1

            if idx == -len(selected):
                idx = random_state.randint(0, len(selected)-1)

            selected_indvs.append(population[idx])
            selected[idx] = False

        return selected_indvs

