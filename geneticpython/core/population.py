"""
# Problem: population.py
# Description: 
# Created by ngocjr7 on [2020-03-29 23:29:36]
"""
from __future__ import absolute_import

from functools import wraps
from typing import List, Union, Callable, Tuple, NewType
from tqdm.auto import tqdm
from random import Random

from .individual import Individual
from geneticpython.utils.validation import check_random_state

import random


class Population():

    def __init__(self, individual_temp: Individual, size: int, init_population: Callable[[], List[Individual]] = None):
        self.individual_temp = individual_temp
        self.size = size
        self.init_population = init_population or self.init_population_randomly
        self.individuals = []

    def __str__(self):
        ret = '[\n'
        for indiv in self.individuals:
            ret += str(indiv) + '\n'
        ret += ']'
        return ret

    def __repr__(self):
        ret = '['
        for indiv in self.individuals:
            ret += str(indiv) + '\n'
        ret += ']'
        return ret

    def __getitem__(self, key):
        '''
        Get individual by index.
        '''
        if key < 0 or key >= len(self.individuals):
            raise IndexError('Individual index({}) out of range'.format(key))
        return self.individuals[key]

    def __len__(self):
        '''
        Get length of population.
        '''
        return len(self.individuals)

    def set_initialization(self, callback: Callable[[], List[Individual]]):
        self.init_population = callback

    def init_population_randomly(self, random_state=None) -> List[Individual]:
        random_state = check_random_state(random_state)
        ret = []
        for _ in range(self.size):
            new_indiv = self.individual_temp.clone()
            new_indiv.random_init(random_state=random_state)
            ret.append(new_indiv)
        return ret

    def clear(self):
        self.individuals.clear()

    def all_objective(self):
        return [indv._objective for indv in self.individuals]

    def all_objectives(self):
        return [indv._objectives for indv in self.individuals]

    def extend(self, others: List[Individual]):
        if len(self.individuals) + len(others) > self.size:
            raise ValueError(
                f"Population size is {self.size}. Out of the limit")
        self.individuals.extend(others)

    def append(self, another: Individual):
        if len(self.individuals) + 1 > self.size:
            raise ValueError(
                f"Population size is {self.size}. Out of the limit")
        self.individuals.append(another)

    def register_initialization(self, fn):
        @wraps(fn)
        def _fn_with_return_checked(random_state=None):
            # Check objective.
            population = fn(random_state)
            is_invalid = not isinstance(population, list) or not all(
                isinstance(indv, Individual) for indv in population)
            if is_invalid:
                msg = 'returned population (type: {}) is invalid,\
                    initialization must return list of Individual'
                msg = msg.format(type(population))
                raise ValueError(msg)
            return population

        self.init_population = _fn_with_return_checked

