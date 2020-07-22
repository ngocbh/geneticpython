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

from ...core.individual import Individual
from ...core.population import Population
from ...core.operators import Selection, Crossover, Mutation, Replacement, RankReplacement
from ..geneticengine import GeneticEngine
from ...callbacks import CallbackList, Callback, History, MultiObjectiveHistory
from .multi_objective_engine import MultiObjectiveEngine

import random
import math
import itertools
import numpy as np


class NSGAIIEngine(MultiObjectiveEngine):

    def __init__(self, population: Population,
                 objectives: List[Callable[[Individual], Union[float, int]]] = None,
                 selection: Selection = None,
                 selection_size: int = None,
                 crossover: Crossover = None,
                 mutation: Mutation = None,
                 callbacks: List[Callback] = None,
                 max_iter: int = 100,
                 random_state: int = None):

        replacement = RankReplacement()

        super(NSGAIIEngine, self).__init__(population=population,
                                           objectives=objectives,
                                           selection=selection,
                                           selection_size=selection_size,
                                           crossover=crossover,
                                           mutation=mutation,
                                           replacement=replacement,
                                           callbacks=callbacks,
                                           max_iter=max_iter,
                                           random_state=random_state)

    @staticmethod
    def crowded_comparator(p1: Individual, p2: Individual) -> int:
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

    @staticmethod
    def nondominated_sort(population: List[Individual]) -> List[List[Individual]]:
        """
            This function uses Individuals.objectives for compararing

            :param population: list of individual
            :type population: List[Individual]

            :return: List of front (List[Individual]) after nondominated sorting
            :rtype: List[List[Individual]]
        """
        def is_dominating(a: Individual, b: Individual) -> bool:

            if len(a._objectives) != len(b._objectives):
                msg = 'The length of objective in two individual is not the same:\
                     a has {} objectives, b has {} objectives'
                msg = msg.format(len(a._objectives), len(b._objectives))
                raise ValueError(msg)

            dominated = False
            for i in range(len(a._objectives)):
                if a._objectives[i] > b._objectives[i]:
                    return False
                elif a._objectives[i] < b._objectives[i]:
                    dominated = True

            return dominated

        fronts = list()
        num_dominators = dict()
        slaves = dict()

        # find fisrt pareto front
        fronts.append(list())
        for p1 in population:
            slaves[p1] = list()
            num_dominators[p1] = 0

            for p2 in population:
                if is_dominating(p1, p2):
                    slaves[p1].append(p2)
                elif is_dominating(p2, p1):
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
    def sort(population: List[Individual]) -> List[Individual]:
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
        population = self.population.init_population(self.rand)

        population = self.do_evaluation(population)
        population = self.sort(population)

        return population

    def do_evaluation(self, population: List[Individual]) -> List[Individual]:
        ret = list()
        # compute objectives
        for indv in population:
            indv._coefficients = self.coefficients
            indv._objectives = list()
            for objective in self.objectives:
                indv._objectives.append(objective(indv))
            ret.append(indv)

        return ret

    def do_reproduction(self, mating_population: List[Individual]) -> List[Individual]:
        childs = []
        for i in range(0, len(mating_population), 2):
            childs_temp = self.crossover.cross(father=mating_population[i],
                                               mother=mating_population[i+1],
                                               rand=self.rand)
            childs.extend(childs_temp)

        for i in range(len(childs)):
            childs[i] = self.mutation.mutate(childs[i], rand=self.rand)

        return childs

    def do_selection(self) -> List[Individual]:
        try:
            mating_population = self.selection.select(self.selection_size,
                                                      population=self.population.individuals,
                                                      comparator=self.crowded_comparator,
                                                      rand=self.rand)
        except TypeError as err:
            raise TypeError(" {}\nSelection does not support nondominated comparator,\n \
                    TournamentSelection is recommended".format(err))

        return mating_population

    def do_replacement(self, new_population) -> List[Individual]:
        new_population = NSGAIIEngine.sort(new_population)

        new_population = self.replacement.replace(
            self.population.size,
            new_population,
            comparator=NSGAIIEngine.crowded_comparator,
            sorted=True,
            rand=self.rand)
        return new_population

    def run(self) -> History:
        return super(NSGAIIEngine, self).run()

    def get_pareto_front(self) -> List[Individual]:
        pareto_front = list()
        for indv in self.population.individuals:
            if indv.nondominated_rank == 0:
                pareto_front.append(indv)

        return pareto_front


if __name__ == '__main__':
    pass
