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

from ..geneticengine import GeneticEngine
from ...callbacks import Callback, CallbackList
from ...callbacks import History, MultiObjectiveHistory
from ...core.population import Population
from ...core.operators import Selection, Crossover, Mutation, Replacement
from ...core.individual import Individual

import math


class MultiObjectiveEngine(GeneticEngine):
    def __init__(self, population: Population,
                 objectives: List[Callable[[Individual], Union[float, int]]] = None,
                 selection: Selection = None,
                 selection_size: int = None,
                 crossover: Crossover = None,
                 mutation: Mutation = None,
                 replacement: Replacement = None,
                 callbacks: List[Callback] = None,
                 max_iter: int = 100,
                 random_state: int = None):
        callback_list = CallbackList(
            callbacks, add_mo_history=True, add_progbar=True)
        super(MultiObjectiveEngine, self).__init__(population=population,
                                                   selection=selection,
                                                   selection_size=selection_size,
                                                   crossover=crossover,
                                                   mutation=mutation,
                                                   replacement=replacement,
                                                   callbacks=callback_list,
                                                   max_iter=max_iter,
                                                   random_state=random_state)

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
