"""
# Filename: rank_replacement.py
# Description:
# Created by ngocjr7 on [12-06-2020 00:25:52]
"""
from __future__ import absolute_import

from .replacement import Replacement
from ...individual import Individual
from geneticpython.utils.validation import check_random_state

from typing import List, Union, Callable
from bisect import bisect_right
from itertools import accumulate
from functools import cmp_to_key

import copy


class RankReplacement(Replacement):
    __EPS = 1e-14

    def single_objective_comparator(self, x: Individual, y: Individual) -> int:
        if x._objective < y._objective:
            return -1
        elif x._objective > y._objective:
            return 1
        else:
            return 0

    def replace(self, size: int, population: List[Individual],
                comparator: Callable[[Individual, Individual], bool] = None,
                sorted: bool = False,
                random_state=None) -> List[Individual]:
        # random_state = check_random_state(random_state)
        if not sorted:
            # sort
            if not comparator:
                comparator = self.single_objective_comparator

            sorted_population = sorted(population, key=cmp_to_key(comparator))

        ret_population = population[:size]
        return ret_population


if __name__ == '__main__':
    pass

