"""
File: scramble_mutation.py
Created by ngocjr7 on 2020-10-05 22:08
Description: 
"""

from __future__ import absolute_import

from geneticpython.models.int_individual import IntIndividual
from geneticpython.core.operators.mutation.mutation import Mutation
from geneticpython.utils.validation import check_random_state

from random import Random
import random
import numpy as np


class ScrambleMutation(Mutation):
    def mutate(self, individual: IntIndividual, random_state=None):
        raise NotImplementedError
