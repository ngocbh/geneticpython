"""
# Problem: uniform_crossover.py
# Description: 
# Created by ngocjr7 on [2020-03-31 15:58:29]
"""
from __future__ import absolute_import

from .crossover import Crossover
from geneticpython.models.int_individual import IntIndividual
from geneticpython.utils.validation import check_random_state

from copy import deepcopy
from random import Random
import random

class UniformCrossover(Crossover):
    def __init__(self, pc, pe=0.5):
        if pe <= 0.0 or pe > 1.0:
            raise ValueError('Invalid genome exchange probability')
        self.pe = pe
        super(UniformCrossover, self).__init__(pc=pc)

    def cross(self, father : IntIndividual, mother : IntIndividual, random_state=None):
        ''' Cross chromsomes of parent using uniform crossover method.
        :param population: Population where the selection operation occurs.
        :type population: :obj:`gaft.components.Population`
        :return: Selected parents (a father and a mother)
        :rtype: list of :obj:`gaft.components.IndividualBase`
        '''
        random_state = check_random_state(random_state)
        do_cross = True if random_state.random() <= self.pc else False

        if not do_cross:
            return father.clone(), mother.clone()

        # Chromsomes for two children.
        chrom1 = deepcopy(father.chromosome)
        chrom2 = deepcopy(mother.chromosome)

        for i in range(father.chromosome.length):
            g1, g2 = chrom1[i], chrom2[i]
            do_exchange = True if random_state.random() <= self.pe else False
            if do_exchange:
                chrom1[i], chrom2[i] = g2, g1

        child1, child2 = father.clone(), father.clone()
        child1.init(chromosome=chrom1)
        child2.init(chromosome=chrom2)

        return child1, child2
