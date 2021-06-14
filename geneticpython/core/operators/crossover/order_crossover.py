from __future__ import absolute_import 

from geneticpython.core.operators.crossover import Crossover
from geneticpython.core.individual import Individual
from geneticpython.models import PermutationIndividual
from geneticpython.utils.validation import check_random_state

from copy import deepcopy
from random import Random
from typing import Callable

import random
import numpy as np

class OrderCrossover(Crossover):
    """OrderCrossover.
    """

    def __init__(self, pc : float):
        super(OrderCrossover, self).__init__(pc=pc)

    def cross(self, father : PermutationIndividual, mother : PermutationIndividual, random_state=None):
        ''' Cross chromsomes of parent using single point crossover method.
        '''
        random_state = check_random_state(random_state)
        do_cross = True if random_state.random() <= self.pc else False

        if not do_cross:
            return father.clone(), mother.clone()

        # Chromsomes for two children.
        chrom1 = deepcopy(father.chromosome)
        chrom2 = deepcopy(mother.chromosome)
        # print(chrom1)
        # print(chrom2)
        if father.chromosome.length != mother.chromosome.length:
            raise ValueError("Father and mother have different length")

        length = father.chromosome.length

        slt_points = list(random_state.choice(length, 2, replace=False))
        slt_points.sort()
        p1, p2 = slt_points
        cs1 = set(father.chromosome.genes[p1:p2])
        cs2 = set(mother.chromosome.genes[p1:p2])

        j1, j2 = 0, 0
        for i in range(length):
            if mother.chromosome[i] not in cs1:
                if j1 == p1:
                    j1 = p2
                chrom1[j1] = mother.chromosome[i]
                j1 += 1
            if father.chromosome[i] not in cs2:
                if j2 == p1:
                    j2 = p2
                chrom2[j2] = father.chromosome[i]
                j2 += 1

        # print(chrom1)
        # print(chrom2)

        child1, child2 = father.clone(), father.clone()
        child1.init(chromosome=chrom1)
        child2.init(chromosome=chrom2)

        return child1, child2
