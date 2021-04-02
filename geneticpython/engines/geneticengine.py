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

from geneticpython.core.individual import Individual
from geneticpython.core.population import Population
from geneticpython.core.operators import Selection, Crossover, Mutation, Replacement
from geneticpython.callbacks import Callback, History, CallbackList
from geneticpython.utils.validation import check_random_state

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
                 generations: int = None,
                 random_state = None):

        self.population = population
        self.generations = generations
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.replacement = replacement
        self.objective = objective
        self.objectives = objectives
        self.selection_size = selection_size or self.population.size
        self.random_state = check_random_state(random_state)
        self.callbacks = callbacks
        self.callbacks.set_engine(self)
        self.metrics = None
        self.history = None
        self.stop_running = False
        self.coefficients = None
        self.coefficient = None

    def set_selection(self, selection: Selection):
        self.selection = selection

    def set_crossover(self, crossover: Crossover):
        self.crossover = crossover

    def set_mutation(self, mutation: Mutation):
        self.mutation = mutation

    def set_replacement(self, replacement: Replacement):
        self.replacement = replacement

    def summary(self):
        pass

    def do_initialization(self) -> List[Individual]:
        population = self.population.init_population(random_state=self.random_state)
        return population

    def do_selection(self) -> List[Individual]:
        return self.selection.select(self.selection_size,
                                     self.population,
                                     random_state=self.random_state)

    def do_reproduction(self, mating_population: List[Individual]) -> List[Individual]:
        childs = []
        for i in range(0, len(mating_population), 2):
            childs_temp = self.crossover.cross(father=mating_population[i],
                                               mother=mating_population[i+1],
                                               random_state=self.random_state)
            childs.extend(childs_temp)

        for i in range(len(childs)):
            childs[i] = self.mutation.mutate(childs[i], random_state=self.random_state)

        return childs

    def do_evaluation(self, population: List[Individual]) -> List[Individual]:
        return population

    def do_replacement(self, new_population: List[Individual]) -> List[Individual]:
        return self.replacement.replace(self.population.size,
                                        new_population,
                                        random_state=self.random_state)

    @abstractmethod
    def compute_objectives(self, population: List[Individual]) -> List[Individual]:
        pass

    def _update_metrics(self) -> None:
        pass

    def _update_logs(self, logs):
        return logs

    def run(self, generations: int = None) -> History:
        if generations is not None:
            self.generations = generations

        logs = None
        self.callbacks.on_running_begin(logs=logs)

        self.callbacks.on_init_population_begin(logs=logs)
        self.population.individuals = self.do_initialization()
        self.population.individuals = self.compute_objectives(
            self.population.individuals)
        self.population.individuals = self.do_evaluation(
            self.population.individuals)
        self._update_metrics()
        logs = self._update_logs(logs)
        self.callbacks.on_init_population_end(logs=logs)

        for gen in range(self.generations):
            self.callbacks.on_generation_begin(gen, logs=logs)

            self.callbacks.on_selection_begin(gen, logs=logs)
            mating_population = self.do_selection()
            self.callbacks.on_selection_end(gen, logs=logs)

            self.callbacks.on_reproduction_begin(gen, logs=logs)
            offspring_population = self.do_reproduction(mating_population)
            self.callbacks.on_reproduction_end(gen, logs=logs)

            offspring_population = self.compute_objectives(
                offspring_population)

            self.callbacks.on_evaluation_begin(gen, logs=logs)
            new_population = self.population.individuals + offspring_population
            new_population = self.do_evaluation(new_population)
            self.callbacks.on_evaluation_end(gen, logs=logs)

            self.callbacks.on_replacement_begin(gen, logs=logs)
            self.population.individuals = self.do_replacement(new_population)
            self.callbacks.on_replacement_end(gen, logs=logs)

            self._update_metrics()
            logs = self._update_logs(logs)

            self.callbacks.on_generation_end(gen, logs=logs)

            if self.stop_running:
                break

        self.callbacks.on_running_end(logs=logs)

        return self.history

    def get_all_solutions(self) -> List[Individual]:
        return self.population.individuals


if __name__ == '__main__':
    pass
