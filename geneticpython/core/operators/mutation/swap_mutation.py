"""
File: swap_mutation.py
Created by ngocjr7 on 2020-10-05 21:38
Description: 
"""

from __future__ import absolute_import

from geneticpython.models.int_individual import IntIndividual
from geneticpython.core.operators.mutation.mutation import Mutation
from geneticpython.utils.validation import check_random_state

from random import Random
import random
import numpy as np


class SwapMutation(Mutation):
    def __init__(self, pm : float, n_points: int = 1):
        if n_points < 1:
            raise ValueError('invalid n_points, require n_points > 0')
        self.n_points = n_points
        super(SwapMutation, self).__init__(pm=pm)

    def mutate(self, individual: IntIndividual, random_state=None):
        random_state = check_random_state(random_state)
        do_mutation = True if random_state.random() <= self.pm else False

        ret_individual = individual.clone()

        if not do_mutation:
            return ret_individual

        length = individual.chromosome.length
        points = np.arange(length-1)
        if self.n_points * 2 > length:
            raise ValueError('SwapMutation: n_points * 2 > length')
        slt_points = random_state.choice(points, self.n_points * 2)

        for i in range(0, len(slt_points), 2):
            x, y = slt_points[i], slt_points[i+1]
            g1, g2 = ret_individual.chromosome[x], ret_individual.chromosome[y]
            ret_individual.chromosome[x], ret_individual.chromosome[y] = g2, g1

        return ret_individual
