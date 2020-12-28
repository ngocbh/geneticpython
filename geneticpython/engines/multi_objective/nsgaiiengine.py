"""
# Filename: nsgaiiengine.py
# Description:
# Created by ngocjr7 on [09-06-2020 16:05:40]
"""
from __future__ import absolute_import

from functools import wraps
from typing import List, Union, Callable, Dict
from random import Random
from tqdm.auto import tqdm

from geneticpython.core import Individual, Population, Pareto
from geneticpython.core.operators import Selection, Crossover, Mutation
from geneticpython.core.operators import Replacement, RankReplacement, TournamentSelection
from geneticpython.engines.geneticengine import GeneticEngine
from geneticpython.callbacks import CallbackList, Callback, History
from geneticpython.engines.multi_objective.multi_objective_engine import MultiObjectiveEngine, is_dominated
from geneticpython.utils.validation import check_random_state

import random
import math
import itertools
import numpy as np


def default_crowded_comparator(p1: Individual, p2: Individual) -> int:
    if p1.nondominated_rank < p2.nondominated_rank:
        return -1
    elif p1.nondominated_rank > p2.nondominated_rank:
        return 1
    else:
        if p1.crowding_distance > p2.crowding_distance:
            return -1
        elif p1.crowding_distance < p2.crowding_distance:
            return 1
        else:
            return 0

class NSGAIIEngine(MultiObjectiveEngine):

    def __init__(self, population: Population,
                 objectives: List[Callable[[Individual], Union[float, int]]] = None,
                 tournament_size: int = 2,
                 selection_size: int = None,
                 crossover: Crossover = None,
                 mutation: Mutation = None,
                 callbacks: List[Callback] = None,
                 generations: int = 100,
                 random_state: int = None,
                 crowded_comparator: Callable[[Individual, Individual], int] = None):

        replacement = RankReplacement()
        selection = TournamentSelection(tournament_size)
        self.crowded_comparator = crowded_comparator or default_crowded_comparator

        super(NSGAIIEngine, self).__init__(population=population,
                                           objectives=objectives,
                                           selection=selection,
                                           selection_size=selection_size,
                                           crossover=crossover,
                                           mutation=mutation,
                                           replacement=replacement,
                                           callbacks=callbacks,
                                           generations=generations,
                                           random_state=random_state)


    @staticmethod
    def nondominated_sort(population: List[Individual]) -> List[List[Individual]]:
        """
            This function uses Individuals.objectives for compararing

            :param population: list of individual
            :type population: List[Individual]

            :return: List of front (List[Individual]) after nondominated sorting
            :rtype: List[List[Individual]]
        """
        fronts = list()
        num_dominators = dict()
        slaves = dict()

        # find fisrt pareto front
        fronts.append(list())
        for p1 in population:
            slaves[p1] = list()
            num_dominators[p1] = 0

            for p2 in population:
                if is_dominated(p1, p2):
                    slaves[p1].append(p2)
                elif is_dominated(p2, p1):
                    num_dominators[p1] += 1

            if num_dominators[p1] == 0:
                fronts[0].append(p1)

        # find other pareto front
        i = 0
        while len(fronts[i]) > 0:
            current_front = list()
            for p1 in fronts[i]:
                for p2 in slaves[p1]:
                    num_dominators[p2] -= 1
                    if num_dominators[p2] == 0:
                        current_front.append(p2)

            i += 1
            fronts.append(current_front)

        if len(fronts[-1]) == 0:
            fronts.pop()

        return fronts

    @staticmethod
    def calc_crowding_distance(front: List[Individual]) -> Dict[Individual, float]:
        """
            compute crowding distance for each individual in pareto front

            :param front: a list of individual in pareto front
            :type front: List[Individual]

            :return: crowding distance of each individual, stored in a dict
            :rtype: Dict[Individual, float]
        """
        crowding_distance = dict()
        n = len(front)
        for i in range(n):
            crowding_distance[front[i]] = 0.0

        for m in range(len(front[0]._objectives)):
            front.sort(key=lambda indv: indv._objectives[m])
            crowding_distance[front[0]
                              ] = crowding_distance[front[n - 1]] = float('inf')
            delta_f = front[n - 1]._objectives[m] - front[0]._objectives[m]
            if delta_f != 0.0:
                for i in range(1, n - 1):
                    crowding_distance[front[i]] += (
                        front[i + 1]._objectives[m] - front[i - 1]._objectives[m]) / delta_f

        return crowding_distance

    @staticmethod
    def sort(population: List[Individual], random_state=None) -> List[Individual]:
        random_state = check_random_state(random_state)
        # non-dominated sorting
        pareto_fronts = NSGAIIEngine.nondominated_sort(population)

        # assign nondominated rank
        for rank in range(len(pareto_fronts)):
            for i in range(len(pareto_fronts[rank])):
                pareto_fronts[rank][i].nondominated_rank = rank

        # compute and assign  crowding distance
        for rank in range(len(pareto_fronts)):
            crowding_distance_dict = NSGAIIEngine.calc_crowding_distance(
                pareto_fronts[rank])
            for i in range(len(pareto_fronts[rank])):
                pareto_fronts[rank][i].crowding_distance = crowding_distance_dict[pareto_fronts[rank][i]]

            random_state.shuffle(pareto_fronts[rank])

            pareto_fronts[rank].sort(
                key=lambda indv: indv.crowding_distance, reverse=True)

        flatten_population = list(itertools.chain.from_iterable(pareto_fronts))

        return flatten_population

    def do_initialization(self) -> List[Individual]:
        # Injecting nondominated_rank and crowding_distance for template individuals
        # This just makes it easier to understand
        self.population.individual_temp.nondominated_rank = None
        self.population.individual_temp.crowding_distance = None
        # init population
        population = self.population.init_population(self.random_state)

        return population

    def do_evaluation(self, population: List[Individual]) -> List[Individual]:
        population = NSGAIIEngine.sort(population, self.random_state)
        return population

    def do_reproduction(self, mating_population: List[Individual]) -> List[Individual]:
        return super(NSGAIIEngine, self).do_reproduction(mating_population)

    def do_selection(self) -> List[Individual]:
        try:
            mating_population = self.selection.select(self.selection_size,
                                                      population=self.population.individuals,
                                                      comparator=self.crowded_comparator,
                                                      random_state=self.random_state)
        except TypeError as err:
            raise TypeError(" {}\nSelection does not support nondominated comparator,\n \
                    TournamentSelection is recommended".format(err))

        return mating_population

    def do_replacement(self, new_population) -> List[Individual]:
        new_population = self.replacement.replace(
            self.population.size,
            new_population,
            comparator=self.crowded_comparator,
            sorted=True,
            random_state=self.random_state)
        return new_population

    def run(self, generations: int = None) -> History:
        return super(NSGAIIEngine, self).run(generations)

    def get_pareto_front(self) -> Pareto:
        pareto_front = list()
        for indv in self.population.individuals:
            try:
                if indv.nondominated_rank == 0:
                    pareto_front.append(indv)
            except:
                raise ValueError(f"Cannot get nondominated_rank from individuals\
                                 The engine has not run yet")

        return Pareto(pareto_front)


if __name__ == '__main__':
    pass
