"""
File: prim_crossover.py
Created by ngocjr7 on 2020-09-10 16:18
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

from __future__ import absolute_import

from geneticpython.core.operators.crossover import Crossover
from geneticpython.core.individual import Individual
from geneticpython.utils.validation import check_random_state
from geneticpython.utils import rset
from geneticpython.models.tree import Tree, RootedTree

from copy import deepcopy
from random import Random
from typing import Callable

import random
import numpy as np

class PrimCrossover(Crossover):

    def cross(self, father: Individual, mother: Individual, random_state=None):
        random_state = check_random_state(random_state)
        do_cross = True if random_state.random() <= self.pc else False

        children = father.clone(), mother.clone()
        if not do_cross:
            return children

        trees = children[0].decode(), children[1].decode()
        if not (isinstance(trees[0], Tree) and isinstance(trees[1], Tree)):
            raise ValueError(f"The PrimCrossover is only used on the individual that \
                             decodes to an instance of Tree. \
                             got father type: {type(trees[0])} and mother type {type(trees[1])}")

        edge_union = set() 
        potential_adj = [list() for _ in range(trees[0].number_of_vertices)]
        for i in range(2):
            for u, v in trees[i].edges:
                if (v, u) not in edge_union:
                    edge_union.add((u, v))
                    potential_adj[u].append(v)
                    potential_adj[v].append(u)

        for i in range(2):
            trees[i].initialize()

            # This is tricky, 
            # I'm trying to make this method can work both cases  
            # one when you add_edge in initialize() function, and one is not
            # I'm using parent attribute to do this. 
            # But this only work when you update parent attribute after add_edge in initialize()
            # or you this crossover method with RootedTree, it supports update parent attribute in add_edge
            if not isinstance(trees[i], RootedTree) and len(trees[i].edges) != 0:
                raise Exception("Unexpected error occurred when running PrimCrossover")

            if trees[i].root is not None:
                root = trees[i].root
            else:
                random_state.randint(0, trees[i].number_of_vertices)

            trees[i].parent[root] = root
            # Set of connected nodes
            C = set()
            # eligible edges
            A = rset()

            # Init tree 
            for u in range(trees[i].number_of_vertices):
                if trees[i].parent[u] != -1:
                    C.add(u)
                    for v in potential_adj[u]:
                        if v not in C:
                            A.add((u, v))

            while len(C) < trees[i].number_of_vertices:
                u, v = A.random_choice(random_state)
                A.remove((u, v))
                if v not in C:
                    trees[i].add_edge(u, v)
                    C.add(v)
                    for w in potential_adj[v]:
                        if w not in C:
                            A.add((v, w))
                if len(A) == 0 and len(C) != trees[i].number_of_vertices:
                    raise ValueError('Cannot create random spanning tree from unconnected tree')
            trees[i].repair()

        try:
            children[0].encode(trees[0])
            children[1].encode(trees[1])
        except NotImplementedError:
            raise ValueError("Cannot call encode method. PrimCrossover requires encode method in Individual")
        except Exception as e:
            raise e

        return children[0], children[1]
