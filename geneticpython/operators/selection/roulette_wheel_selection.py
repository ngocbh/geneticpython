"""
# Problem: roulette_wheel_selection.py
# Description: 
# Created by ngocjr7 on [2020-03-31 14:55:40]
"""
from __future__ import absolute_import

from .selection import Selection

from bisect import bisect_right
from itertools import accumulate
from random import random

class RouletteWheelSelection(Selection):
    def __init__(self):
        pass

    def select(self, slt_size, population, fitness_func, rand=None, is_unique=False):
        fits = population.all_fits(fitness_func)
        min_fit = min(fits)
        fits = [(e_fit - min_fit + 1) for e_fit in fits]
        sum_fit = sum(fits)
        wheel = list(accumulate([i/sum_fit for i in fits]))

        selected_indvs = []
        for _ in range(slt_size):
            idx = bisect_right(wheel, rand.random())
            selected_indvs.append(population[idx])

        return selected_indvs