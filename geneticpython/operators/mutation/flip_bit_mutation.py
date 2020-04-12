"""
# Problem: flip_bit_mutation.py
# Description: 
# Created by ngocjr7 on [2020-03-31 16:49:14]
"""
from __future__ import absolute_import

from ...individual import BinaryIndividual
from .mutation import Mutation
import random
class FlipBitMutation(Mutation):
    def __init__(self, pm):
        if pm <= 0.0 or pm > 1.0:
            raise ValueError('Invalid mutation probability')

        self.pm = pm

    def mutate(self, individual, rand):
        if not rand:
            rand = random.Random()
        do_mutation = True if rand.random() <= self.pm else False

        # print(individual)
        if do_mutation:
            for i, genome in enumerate(individual.chromosome.genes):
                no_flip = True if rand.random() > self.pm else False
                if no_flip:
                    continue

                # if type(individual) is BinaryIndividual:
                individual.chromosome.genes[i].value = genome.value^1
                # else:
                #     raise TypeError('Wrong individual type: {}'.format(type(individual)))
        # print(individual)
        return individual