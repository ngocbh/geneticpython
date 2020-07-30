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

from ...core.individual import Individual
from ...core.population import Population
from ...core.operators import Selection, Crossover, Mutation, Replacement
from ..geneticengine import GeneticEngine
from .single_objective_engine import SingleObjectiveEngine
from ...callbacks import Callback, History, CallbackList

import random
import math
import copy


class GAEngine(SingleObjectiveEngine):

    def do_initialization(self) -> List[Individual]:
        return super(GAEngine, self).do_initialization()

    def do_selection(self) -> List[Individual]:
        return super(GAEngine, self).do_selection()

    def do_reproduction(self, mating_population: List[Individual]) -> List[Individual]:
        return super(GAEngine, self).do_reproduction(mating_population)

    def do_evaluation(self, population: List[Individual]) -> List[Individual]:
        return super(GAEngine, self).do_evaluation(population)

    def do_replacement(self, new_population: List[Individual]) -> List[Individual]:
        return super(GAEngine, self).do_replacement(new_population)

    def run(self, generations: int = None) -> History:
        return super(GAEngine, self).run(generations)


if __name__ == "__main__":
    pass
