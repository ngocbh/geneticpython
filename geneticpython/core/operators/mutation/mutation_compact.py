"""
File: mutation_compact.py
Created by ngocjr7 on 2020-09-15 21:20
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

from __future__ import absolute_import

from geneticpython.core.individual import Individual
from geneticpython.core.operators.mutation import Mutation
from geneticpython.utils.validation import check_random_state

from typing import List
from itertools import accumulate
from bisect import bisect_right

class MutationCompact(Mutation):
    def __init__(self, mutation_list : List[Mutation] = None, pm_list : List[float] = None):
        mutation_list = mutation_list or []
        pm_list = pm_list or []

        if len(mutation_list) != len(pm_list):
            raise ValueError(f'mutation_list and pm_list must have same length,\n\
                             given mutation_list:{len(mutation_list)} and pm_list:{len(pm_list)}')
        self.pm_list = pm_list
        if any(pm < 0.0 or pm > 1.0 for pm in pm_list):
            raise ValueError('Invalid mutation probability')

        if len(pm_list) > 0:
            self.acc_pm = list(accumulate(pm_list)) 
        else:
            self.acc_pm = []

        if len(self.acc_pm) > 0 and self.acc_pm[-1] > 1.0:
            raise ValueError('Invalid pm_list, accumulation of mutation probability is greater than 1.0')

        self.mutation_list = mutation_list

    def add_mutation(self, mutation : Mutation, pm : float):
        if pm < 0.0 or pm > 1.0:
            raise ValueError('Invalid mutation probability')
        self.pm_list.append(pm)
        s = self.acc_pm[-1] if len(self.acc_pm) > 0 else 0
        if s + pm > 1.0:
            raise ValueError('Invalid pm, accumulation of mutation probability is greater than 1.0')
        self.acc_pm.append(s + pm)
        self.mutation_list.append(mutation)

    def mutate(self, indv : Individual, random_state=None):
        random_state = check_random_state(random_state)
        idx = bisect_right(self.acc_pm, random_state.random())
        if idx >= len(self.mutation_list):
            return indv.clone()

        ret_indv = self.mutation_list[idx].mutate(indv, random_state)
        return ret_indv
