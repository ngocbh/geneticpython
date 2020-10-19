"""
File: multi_objective_engine.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

from __future__ import absolute_import

from typing import Union, Callable, List
from functools import wraps
from abc import ABC, abstractmethod

from ..geneticengine import GeneticEngine
from ...callbacks import Callback, CallbackList
from ...callbacks import History
from ...core.population import Population
from ...core.operators import Selection, Crossover, Mutation, Replacement
from ...core.individual import Individual

import math


def is_dominated(a: Individual, b: Individual) -> bool:
    """
        Return True if a dominate b, otherwise return False
    """
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


class MultiObjectiveEngine(GeneticEngine):
    def __init__(self, population: Population,
                 objectives: List[Callable[[Individual], Union[float, int]]] = None,
                 selection: Selection = None,
                 selection_size: int = None,
                 crossover: Crossover = None,
                 mutation: Mutation = None,
                 replacement: Replacement = None,
                 callbacks: List[Callback] = None,
                 generations: int = 100,
                 random_state: int = None):
        callback_list = CallbackList(
            callbacks, add_history=True, add_progbar=True)
        super(MultiObjectiveEngine, self).__init__(population=population,
                                                   selection=selection,
                                                   selection_size=selection_size,
                                                   crossover=crossover,
                                                   mutation=mutation,
                                                   replacement=replacement,
                                                   callbacks=callback_list,
                                                   generations=generations,
                                                   random_state=random_state)

    @abstractmethod
    def get_pareto_front(self) -> List[Individual]:
        pass

    def _update_logs(self, logs):
        logs = logs or {}
        pareto_front = [
            indv.objectives for indv in self.get_pareto_front()]
        logs.update({'pareto_front': pareto_front})
        solutions = [indv.objectives for indv in self.get_all_solutions()]
        logs.update({'solutions': solutions})
        return logs

    def compute_objectives(self, population: List[Individual]) -> List[Individual]:
        ret = list()
        # compute objectives
        for i in range(len(population)):
            indv = population[i]
            if self.objectives is None:
                raise ValueError(
                    f"Engine has no registered objective functions")
            indv._coefficients = self.coefficients
            indv._objectives = list()
            for objective in self.objectives:
                indv._objectives.append(objective(indv))
            ret.append(indv)
        return ret


    def minimize_objective(self, fn):
        """
            register objective function
        """
        @wraps(fn)
        def _fn_minimization_with_objective_check(indv):
            '''
            A wrapper function for objective function with objective value check.
            '''
            # Check indv type.
            if not isinstance(indv, Individual):
                raise TypeError(
                    'indv\'s class must be subclass of IndividualBase')

            # Check objective.
            objective = float(fn(indv))
            is_invalid = not isinstance(
                objective, (float, int)) or (math.isnan(objective))
            if is_invalid:
                msg = 'objective value(value: {}, type: {}) is invalid'
                msg = msg.format(objective, type(objective))
                raise ValueError(msg)
            return objective

        if not self.objectives:
            self.objectives = [_fn_minimization_with_objective_check]
            self.coefficients = [1]
        else:
            self.objectives.append(_fn_minimization_with_objective_check)
            self.coefficients.append(1)

    def maximize_objective(self, fn):
        """
            register maximization of objective function
        """
        @wraps(fn)
        def _fn_maximization_with_objective_check(indv):
            '''
            A wrapper function for objective function with objective value check.
            '''
            # Check indv type.
            if not isinstance(indv, Individual):
                raise TypeError(
                    'indv\'s class must be subclass of IndividualBase')

            # Check objective.
            objective = float(fn(indv))
            is_invalid = not isinstance(
                objective, (float, int)) or (math.isnan(objective))
            if is_invalid:
                msg = 'objective value(value: {}, type: {}) is invalid'
                msg = msg.format(objective, type(objective))
                raise ValueError(msg)
            return -objective

        if not self.objectives:
            self.objectives = [_fn_maximization_with_objective_check]
            self.coefficients = [-1]
        else:
            self.objectives.append(_fn_maximization_with_objective_check)
            self.coefficients.append(-1)
