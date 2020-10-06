"""
# Problem: flip_bit_mutation.py
# Description: 
# Created by ngocjr7 on [2020-03-31 16:49:14]
"""
from __future__ import absolute_import

from geneticpython.models.binary_individual import BinaryIndividual
from .mutation import Mutation
from geneticpython.utils.validation import check_random_state

from random import Random
import random


class FlipBitMutation(Mutation):
    def __init__(self, pm : float, pe : float = None):
        super(FlipBitMutation, self).__init__(pm=pm)
        if pe is None:
            pe = pm
            
        if pe <= 0.0 or pe > 1.0:
            raise ValueError('Invalid mutation probability')
        self.pe = pe

    def mutate(self, individual: BinaryIndividual, random_state=None):
        random_state = check_random_state(random_state)
        do_mutation = True if random_state.random() <= self.pm else False

        ret_individual = individual.clone()

        if do_mutation:
            for i, genome in enumerate(ret_individual.chromosome.genes):
                flip = True if random_state.random() <= self.pe else False
                if flip:
                    ret_individual.chromosome.genes[i] = genome^1

        return ret_individual
