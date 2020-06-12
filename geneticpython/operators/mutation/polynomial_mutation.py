"""
# Filename: polynomial_mutation.py
# Description:
# Created by ngocjr7 on [11-06-2020 21:56:16]
"""
from __future__ import absolute_import

from ...individual import FloatIndividual
from .mutation import Mutation
from copy import deepcopy
from random import Random
import random
import numpy as np

class PolynomialMutation(Mutation):
    
    def __init__(self, pm: float = None, distribution_index: float = 20):
        if pm <= 0.0 or pm > 1.0:
            raise ValueError('Invalid mutation probability')
        self.pm = pm

        if distribution_index < 0: 
            raise ValueError('Invalid distribution index (must be non-negative)')
        self.distribution_index = distribution_index
        

    def mutate(self, indv: FloatIndividual, rand : Random = Random()):

        ret_indv = indv.clone()

        genes = np.copy(ret_indv.chromosome.genes)
        length = ret_indv.chromosome.length

        xl, xu = ret_indv.chromosome.lower_bound, ret_indv.chromosome.upper_bound
        
        do_mutation = np.array([rand.random() for _ in range(length)]) < self.pm
        genes = genes[do_mutation]
        xl = xl[do_mutation]
        xu = xu[do_mutation]

        delta1 = (genes - xl) / (xu - xl)
        delta2 = (xu - genes) / (xu - xl)

        mut_pow = 1.0 / (self.distribution_index + 1.0)

        u = np.array([rand.random() for _ in range(genes.shape[0])])

        mask = u <= 0.5
        mask_not = np.logical_not(mask)

        deltaq = np.zeros(genes.shape)

        xy = 1.0 - delta1
        val = 2.0 * u + (1.0 - 2.0 * u) * (np.power(xy, (self.distribution_index + 1.0)))
        d = np.power(val, mut_pow) - 1.0
        deltaq[mask] = d[mask]

        xy = 1.0 - delta2
        val = 2.0 * (1.0 - u) + 2.0 * (u - 0.5) * (np.power(xy, (self.distribution_index + 1.0)))
        d = 1.0 - (np.power(val, mut_pow))
        deltaq[mask_not] = d[mask_not]

        mutated_genes = genes + deltaq * (xu - xl)

        # fix out of boudary error
        mutated_genes[mutated_genes < xl] = xl[mutated_genes < xl]
        mutated_genes[mutated_genes > xu] = xu[mutated_genes > xu]

        ret_genes = ret_indv.chromosome.genes
        ret_genes[do_mutation] = mutated_genes

        ret_indv.update_genes(ret_genes)

        return ret_indv







if __name__ == '__main__':
    pass