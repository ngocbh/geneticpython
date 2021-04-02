"""
File: single_objective_engine.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

from __future__ import absolute_import

from typing import List, Union, Callable
from functools import wraps
from collections import OrderedDict

from ..geneticengine import GeneticEngine
from ...core.population import Population
from ...core.operators import Selection, Crossover, Mutation, Replacement
from ...core.individual import Individual
from ...callbacks import Callback, CallbackList
from ...callbacks import History
import math


class SingleObjectiveEngine(GeneticEngine):
    def __init__(self, population: Population,
                 objective: Callable[[Individual], Union[float, int]] = None,
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
        super(SingleObjectiveEngine, self).__init__(population=population,
                                                    objective=objective,
                                                    selection=selection,
                                                    selection_size=selection_size,
                                                    crossover=crossover,
                                                    mutation=mutation,
                                                    replacement=replacement,
                                                    callbacks=callback_list,
                                                    generations=generations,
                                                    random_state=random_state)

    def get_best_indv(self) -> Individual:
        best_indv = min(self.population.individuals,
                        key=lambda indv: indv._objective)
        return best_indv.clone()

    def _update_metrics(self):
        self.metrics = self.metrics or OrderedDict()
        self.metrics['best_objective'] = self.get_best_indv().objective

    def _update_logs(self, logs):
        logs = logs or {}
        logs.update(self.metrics or OrderedDict())
        return logs

    def compute_objectives(self, population: List[Individual]) -> List[Individual]:
        ret = list()
        # compute objectives
        for indv in population:
            if self.objective is None:
                raise ValueError(f"Engine has no registered objective functions")
            indv._coefficient = self.coefficient
            indv._objective = self.objective(indv)
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
        self.objective = _fn_minimization_with_objective_check
        self.coefficient = 1

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
        self.objective = _fn_maximization_with_objective_check
        self.coefficient = -1
