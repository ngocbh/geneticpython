"""
# Filename: sbx_crossover.py
# Description:
# Created by ngocjr7 on [11-06-2020 11:29:04]
"""
from __future__ import absolute_import

from .crossover import Crossover
from geneticpython.models.float_individual import FloatIndividual
from geneticpython.utils.validation import check_random_state

from copy import deepcopy
from random import Random
import random
import numpy as np

class SBXCrossover(Crossover):
    __EPS = 1.0e-14
    """
        This code implement simulated binary crossover from this paper
        (1) AZEVEDO, Carlos Renato Belo. Geração de diversidade na otimização 
        dinâmica multiobjetivo evolucionária por paisagens de não-dominância. 
        2011. Dissertação de Mestrado. Universidade Federal de Pernambuco.
            c1 = 0.5 * (father + mother) - beta * abs(father - mother)
            c2 = 0.5 * (father + mother) + beta * abs(father - mother)

            beta is a vector of random variables which is calculated by following formula:
            u = random(0,1)
            beta[i] = (2*u)^(1/(n+1)) if u < 0.5
                    or (1/(2*(1-u)))^(1/(n+1)) otherwise
            
            n is index of user defined distribution (not negative)
            NOTE: the strategy above is used for understanding
            this class below is implemented based on open source: 
            https://github.com/msu-coinlab/pymoo/blob/master/pymoo/operators/crossover/simulated_binary_crossover.py
    """
    def __init__(self, pc : float, distribution_index : float = 5.0):
        if distribution_index < 0: 
            raise ValueError('Invalid distribution index (must be non-negative)')
        self.distribution_index = distribution_index
        super(SBXCrossover, self).__init__(pc=pc)

    def cross(self, father : FloatIndividual, mother : FloatIndividual, random_state=None):
        random_state = check_random_state(random_state)
        do_crossover = True if random_state.random() <= self.pc else False

        if not do_crossover:
            return father.clone(), mother.clone()

        length = father.chromosome.length
        xl, xu = father.chromosome.lower_bound, father.chromosome.upper_bound

        # Chromsomes for two children.
        y1 = deepcopy(father.chromosome.genes)
        y2 = deepcopy(mother.chromosome.genes)
        
        cross_element = np.full(length, True)
        cross_element[random_state.random(length) > self.pc] = False
        cross_element[np.abs(y1 - y2) <= self.__EPS] = False

        # ensure chromo1 < chromo2
        for i in range(length):
            if y1[i] > y2[i]:
                y1[i], y2[i] = y2[i], y1[i]
        
        u = random_state.random(length)

        def calc_betaq(beta):
            alpha = 2.0 - np.power(beta, -(self.distribution_index + 1.0))

            mask, mask_not = (u <= (1.0 / alpha)), (u > (1.0 / alpha))
            betaq = np.zeros(mask.shape)
            betaq[mask] = np.power((u * alpha), (1.0 / (self.distribution_index + 1.0)))[mask]
            betaq[mask_not] = np.power((1.0 / (2.0 - u * alpha)), (1.0 / (self.distribution_index + 1.0)))[mask_not]

            return betaq

        delta = (y2 - y1)
        delta[delta < 1.0e-10] = 1.0e-10

        beta = 1.0 + (2.0 * (y1 - xl) / delta)
        betaq = calc_betaq(beta)
        c1 = 0.5 * ((y1 + y2) - betaq * delta)

        beta = 1.0 + (2.0 * (xu - y2) / delta)
        betaq = calc_betaq(beta)
        c2 = 0.5 * ((y1 + y2) + betaq * delta)

        # do randomly a swap of variables
        b = random_state.random(length) <= 0.5
        val = np.copy(c1[b])
        c1[b] = c2[b]
        c2[b] = val

        genes1 = np.copy(father.chromosome.genes)
        genes2 = np.copy(mother.chromosome.genes)

        # copy the positions where the crossover was done
        genes1[cross_element] = c1[cross_element]
        genes2[cross_element] = c2[cross_element]

        # repair boundary
        genes1[genes1 < xl] = xl[genes1 < xl]
        genes1[genes1 > xu] = xu[genes1 > xu]

        genes2[genes2 < xl] = xl[genes2 < xl]
        genes2[genes2 > xu] = xu[genes2 > xu]

        offspring1, offspring2 = father.clone(), mother.clone()

        offspring1.update_genes(genes1)
        offspring2.update_genes(genes2)

        return offspring1, offspring2


if __name__ == '__main__':
    pass
