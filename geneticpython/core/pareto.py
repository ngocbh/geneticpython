from typing import List, Union, Callable, Tuple, NewType
from tqdm.auto import tqdm
from random import Random

from .individual import Individual

class Pareto():
    def __init__(self, population: List[Individual] = None):
        self.individuals = population or []

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

    def clear(self):
        self.individuals.clear()

    def all_objective(self):
        return [indv._objective for indv in self.individuals]

    def all_objectives(self):
        return [indv._objectives for indv in self.individuals]

    def extend(self, others: List[Individual]):
        self.individuals.extend(others)

    def append(self, another: Individual):
        self.individuals.append(another)
