"""
File: kruskal_crossover.py
Created by ngocjr7 on 2020-08-26 15:38
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

from __future__ import absolute_import

from geneticpython.core.operators.crossover import Crossover
from geneticpython.core.individual import Individual
from geneticpython.utils.validation import check_random_state
from geneticpython.models.tree import KruskalTree

from copy import deepcopy
from random import Random
from typing import Callable

import random
import sys
import numpy as np


class KruskalCrossover(Crossover):
    """
    KruskalCrossover: Only use on the individual that decodes to a KruskalTree

        params:
        :pc: probability of crossover
    """

    def __init__(self, pc: float):
        super(KruskalCrossover, self).__init__(pc=pc)

    def cross(self, father: Individual, mother: Individual, random_state=None):
        """ Cross chromsomes of parent using kruskal crossover method.
            + join 2 tree
            + keep the edges that appear in both
            + random weight for the remaining edges
            + use kruskal algorithm create offspring 1
            + random another weight for the remaining edges
            + use kruskal algorithm to create offspring 2
        """
        random_state = check_random_state(random_state)
        do_cross = True if random_state.random() <= self.pc else False

        if not do_cross:
            return father.clone(), mother.clone()

        tree1, tree2 = father.decode(), mother.decode()
        if not (isinstance(tree1, KruskalTree) and isinstance(tree2, KruskalTree)):
            raise ValueError(f"The KruskalCrossover is only used on the individual that \
                             decodes to an instance of KruskallTree. \
                             got father type: {type(tree1)} and mother type {type(tree2)}")

        intersection = set()
        remaining_edges = set()
        tree1_edges = set(tree1.edges)
        tree2_edges = set(tree2.edges)

        for u, v in tree1_edges:
            if (u, v) in tree2_edges or (v, u) in tree2_edges:
                intersection.add((u, v))
            elif (v, u) not in remaining_edges:
                remaining_edges.add((u, v))

        for u, v in tree2_edges:
            if (u, v) not in tree1_edges and (v, u) not in tree1_edges \
                    and (v, u) not in remaining_edges:
                remaining_edges.add((u, v))

        remaining_edges = list(remaining_edges)
        children = [tree1.clone(), tree2.clone()]

        for i in range(len(children)):
            # renew offspring tree
            children[i].initialize()
            # add edges that appear in both tree to offsprings
            for u, v in intersection:
                children[i].add_edge(u, v)

            # random weight for remaining_edges
            order = random_state.permutation(np.arange(len(remaining_edges)))
            for j in order:
                u, v = remaining_edges[j]
                children[i].add_edge(u, v)

            children[i].repair()

        offspring1, offspring2 = father.clone(), mother.clone()
        try:
            offspring1.encode(children[0])
            offspring2.encode(children[1])
        except NotImplementedError:
            raise ValueError("Cannot call encode method. PrimCrossover requires encode method in Individual")
        except Exception as e:
            raise e
            
        return offspring1, offspring2
                


