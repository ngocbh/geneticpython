"""
# Problem: uniform_crossover.py
# Description: 
# Created by ngocjr7 on [2020-03-31 15:58:29]
"""
from __future__ import absolute_import

from .crossover import Crossover
from geneticpython.models.binary_individual import BinaryIndividual
from copy import deepcopy
from random import Random
import random

class UniformCrossover(Crossover):
    def __init__(self, pc, pe=0.5):
        if pc <= 0.0 or pc > 1.0:
            raise ValueError('Invalid crossover probability')
        self.pc = pc

        if pe <= 0.0 or pe > 1.0:
            raise ValueError('Invalid genome exchange probability')
        self.pe = pe

    def cross(self, father : BinaryIndividual, mother : BinaryIndividual, rand : Random = Random()):
        ''' Cross chromsomes of parent using uniform crossover method.
        :param population: Population where the selection operation occurs.
        :type population: :obj:`gaft.components.Population`
        :return: Selected parents (a father and a mother)
        :rtype: list of :obj:`gaft.components.IndividualBase`
        '''
        do_cross = True if rand.random() <= self.pc else False

        if not do_cross:
            return father.clone(), mother.clone()

        # Chromsomes for two children.
        chrom1 = deepcopy(father.chromosome)
        chrom2 = deepcopy(mother.chromosome)

        for i in range(father.chromosome.length):
            g1, g2 = chrom1[i], chrom2[i]
            do_exchange = True if rand.random() <= self.pe else False
            if do_exchange:
                chrom1[i], chrom2[i] = g2, g1

        child1, child2 = father.clone(), father.clone()
        child1.init(chromosome=chrom1)
        child2.init(chromosome=chrom2)

        return child1, child2
