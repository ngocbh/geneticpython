"""
# Problem: geneticengine.py
# Description: 
# Created by ngocjr7 on [2020-03-29 22:58:36]
"""
from __future__ import absolute_import

from functools import wraps
from typing import List, Union, Callable
from tqdm.auto import tqdm
from collections import OrderedDict

from ..individual import Individual
from ..population import Population
from ..operators import Selection, Crossover, Mutation, Replacement
from .geneticengine import GeneticEngine
from ..callbacks import Callback, History, SingleObjectiveHistory, CallbackList

import random
import math
import copy


class GAEngine(GeneticEngine):
    def __init__(self, population: Population,
                 objective: Callable[[Individual], Union[float, int]] = None,
                 selection: Selection = None,
                 selection_size: int = None,
                 crossover: Crossover = None,
                 mutation: Mutation = None,
                 replacement: Replacement = None,
                 callbacks: List[Callback] = None,
                 max_iter: int = 100,
                 random_state: int = None):

        callback_list = CallbackList(
            callbacks, add_so_history=True, add_progbar=True)
        super(GAEngine, self).__init__(population=population,
                                       objective=objective,
                                       selection=selection,
                                       selection_size=selection_size,
                                       crossover=crossover,
                                       mutation=mutation,
                                       replacement=replacement,
                                       callbacks=callback_list,
                                       max_iter=max_iter,
                                       random_state=random_state)

    def do_initialization(self) -> List[Individual]:
        population = self.population.init_population(rand=self.rand)
        population = self.do_evaluation(population)
        return population

    def do_selection(self) -> List[Individual]:
        return self.selection.select(self.selection_size,
                                     self.population,
                                     rand=self.rand)

    def do_reproduction(self, mating_population: List[Individual]) -> List[Individual]:
        childs = []
        for i in range(0, len(mating_population), 2):
            childs_temp = self.crossover.cross(
                father=mating_population[i], mother=mating_population[i+1], rand=self.rand)
            childs.extend(childs_temp)

        for i in range(len(childs)):
            childs[i] = self.mutation.mutate(childs[i], rand=self.rand)

        return childs

    def do_evaluation(self, population: List[Individual]) -> List[Individual]:
        ret = list()
        for indv in population:
            indv._objective = self.objective(indv)
            indv._coefficient = self.coefficient
            ret.append(indv)
        return ret

    def do_replacement(self, new_population: List[Individual]) -> List[Individual]:
        return self.replacement.replace(self.population.size,
                                        new_population,
                                        rand=self.rand)

    def _update_metrics(self):
        self.metrics = self.metrics or OrderedDict()
        self.metrics['best_objective'] = self.get_best_indv().objective

    def get_best_indv(self) -> Individual:
        best_indv = min(self.population.individuals,
                        key=lambda indv: indv._objective)
        return best_indv.clone()

    def run(self) -> History:
        return super(GAEngine, self).run()


if __name__ == "__main__":
    pass
