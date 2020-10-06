"""
File: single_point_crossover.py
Created by ngocjr7 on 2020-08-23 20:24
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""
from __future__ import absolute_import 

from geneticpython.core.operators.crossover import Crossover
from geneticpython.core.individual import Individual
from geneticpython.utils.validation import check_random_state

from copy import deepcopy
from random import Random
from typing import Callable

import random
import numpy as np

class PointCrossover(Crossover):
    """
        n point crossover

        params:
        :pc: probability of crossover
        :point_filter: Callable[[int], bool]: filter points that can be crossed
            :parameters: point id, [0, length-1)
            :return: True if point id can be used to cross, False otherwise
    """
    def __init__(self, pc, n_points: int, point_filter : Callable[[int], bool] = lambda x: True):
        self.point_filter = np.vectorize(point_filter)
        self.n_points = n_points
        super(PointCrossover, self).__init__(pc=pc)

    def cross(self, father : Individual, mother : Individual, random_state=None):
        ''' Cross chromsomes of parent using single point crossover method.
        '''
        random_state = check_random_state(random_state)
        do_cross = True if random_state.random() <= self.pc else False

        if not do_cross:
            return father.clone(), mother.clone()

        # Chromsomes for two children.
        chrom1 = deepcopy(father.chromosome)
        chrom2 = deepcopy(mother.chromosome)
        if father.chromosome.length != mother.chromosome.length:
            raise ValueError("Father and mother have different length")

        length = father.chromosome.length

        points = np.arange(length-1)
        points = points[self.point_filter(points)]
        slt_points = list(random_state.choice(points, self.n_points))
        slt_points.append(length)
        slt_points.sort()

        do_exchange = False
        j = 0
        for i in range(father.chromosome.length):
            if i > slt_points[j]:
                do_exchange ^= 1
                j += 1
            if do_exchange:
                chrom1[i], chrom2[i] = chrom2[i], chrom1[i]

        child1, child2 = father.clone(), father.clone()
        child1.init(chromosome=chrom1)
        child2.init(chromosome=chrom2)

        return child1, child2
