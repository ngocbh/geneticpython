"""
# Filename: geneticengine.py
# Description:
# Created by ngocjr7 on [15-07-2020 17:08:13]
"""
from __future__ import absolute_import

from abc import ABC, abstractmethod
from functools import wraps
from typing import List, Union, Callable
from tqdm.auto import tqdm

from ..core.individual import Individual
from ..core.population import Population
from ..core.operators import Selection, Crossover, Mutation, Replacement
from ..callbacks import Callback, History, CallbackList

import random
import math
import copy


class GeneticEngine(ABC):
    def __init__(self, population: Population,
                 objective: Callable[[Individual], Union[float, int]] = None,
                 objectives: List[Callable[[Individual], Union[float, int]]] = None,
                 selection: Selection = None,
                 selection_size: int = None,
                 crossover: Crossover = None,
                 mutation: Mutation = None,
                 replacement: Replacement = None,
                 callbacks: CallbackList = None,
                 max_iter: int = 100,
                 random_state: int = None):

        self.population = population
        self.MAX_ITER = max_iter
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.replacement = replacement
        self.objective = objective
        self.objectives = objectives

        self.selection_size = selection_size or self.population.size

        if random_state:
            self.rand = random.Random(random_state)
        else:
            self.rand = random.Random()

        self.callbacks = callbacks
        self.callbacks.set_engine(self)
        self.metrics = None

    def create_seed(self, seed: int):
        self.rand = random.Random(seed)

    def set_selection(self, selection: Selection):
        self.selection = selection

    def set_crossover(self, crossover: Crossover):
        self.crossover = crossover

    def set_mutation(self, mutation: Mutation):
        self.mutation = mutation

    def set_replacement(self, replacement: Replacement):
        self.replacement = replacement

    @abstractmethod
    def do_initialization(self) -> List[Individual]:
        pass

    @abstractmethod
    def do_selection(self) -> List[Individual]:
        pass

    @abstractmethod
    def do_reproduction(self, mating_population: List[Individual]) -> List[Individual]:
        pass

    @abstractmethod
    def do_evaluation(self, population: List[Individual]) -> List[Individual]:
        pass

    @abstractmethod
    def do_replacement(self, new_population: List[Individual]) -> List[Individual]:
        pass

    def _update_metrics(self):
        pass

    def run(self) -> History:
        self.callbacks.on_running_begin()

        self.callbacks.on_init_population_begin()
        self.population.individuals = self.do_initialization()
        self.callbacks.on_init_population_end()

        for gen in range(self.MAX_ITER):
            self.callbacks.on_generation_begin(gen)
            self.callbacks.on_selection_begin(gen)
            mating_population = self.do_selection()
            self.callbacks.on_selection_end(gen)

            self.callbacks.on_reproduction_begin(gen)
            offspring_population = self.do_reproduction(mating_population)
            self.callbacks.on_reproduction_end(gen)

            self.callbacks.on_evaluation_begin(gen)
            offspring_population = self.do_evaluation(offspring_population)
            self.callbacks.on_evaluation_end(gen)

            new_population = self.population.individuals + offspring_population

            self.callbacks.on_replacement_begin(gen)
            self.population.individuals = self.do_replacement(new_population)
            self.callbacks.on_replacement_end(gen)

            self._update_metrics()

            self.callbacks.on_generation_end(gen)

        self.callbacks.on_running_end()

        return self.callbacks._history

    def get_all_solutions(self) -> List[Individual]:
        return self.population.individuals


if __name__ == '__main__':
    pass
