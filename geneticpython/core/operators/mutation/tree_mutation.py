"""
File: tree_mutation.py
Created by ngocjr7 on 2020-09-07 15:19
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""
from __future__ import absolute_import

from geneticpython.core import Individual
from geneticpython.models.tree import Tree, RootedTree
from geneticpython.utils.validation import check_random_state
from .mutation import Mutation

from typing import List, Tuple
from copy import deepcopy

import numpy as np

class TreeMutation(Mutation):
    """TreeMutation.
    Algorithm:
        Random choose an edge, add to tree. 
        Tree get up a cycle, find cycle and randomly remove one edge in the cycle
    """

    def __init__(self, pm, potential_edges : List[Tuple]):
        """__init__.

        Args:
            pm: probability of mutation
            potential_edges (List[Tuple]): a list of potential edges on graph
        """
        super(TreeMutation, self).__init__(pm=pm)
        self.potential_edges = set()
        for u, v in potential_edges:
            if (u, v) not in self.potential_edges and (v, u) not in self.potential_edges:
                self.potential_edges.add( (u,v) )
        self.potential_edges = list(self.potential_edges)


    def mutate(self, indv: Individual, random_state=None):
        # make sure random_state is not None
        random_state = check_random_state(random_state)

        ret_indv = indv.clone()
        
        # if not do mutation, return the cloner of indv
        if random_state.random() >= self.pm:
            return ret_indv

        # decode individual to get a tree representation
        tree = ret_indv.decode()

        # make sure it is an instance of Tree
        if not isinstance(tree, Tree):
            raise ValueError(f"TreeMutation is only used on the individual\
                             that decode to an instance of Tree,\
                             got {type(tree)}")

        # copy the edges of previous tree
        edges = list(tree.edges)

        # find unused edges in tree, used to choose new edge
        unused_edges = list()
        tree_edges = set(tree.edges)

        for u, v in self.potential_edges: 
            if (u, v) not in tree_edges and (v, u) not in tree_edges:
                unused_edges.append((u, v))

        # choose new edge
        idx = random_state.randint(0, len(unused_edges))
        new_edge = unused_edges[idx]

        # find cycle path after create new edge
        path = tree.find_path(source=new_edge[0], destination=new_edge[1])

        # choose random edge on cycle to remove (break cycle)
        idx = random_state.randint(0, len(path)-1)
        removed_edge = (path[idx], path[idx+1])

        if removed_edge in edges:
            edges.remove(removed_edge)
        else:
            edges.remove((removed_edge[1], removed_edge[0]))

        edges.append(new_edge)

        if isinstance(tree, RootedTree):
            edges = tree.sort_by_bfs_order(edges)
            
        # make new tree from edges
        tree.initialize()
        for u, v in edges:
            tree.add_edge(u, v)

        tree.repair()

        # reencode tree to ret_indv
        try:
            ret_indv.encode(tree)
        except NotImplementedError:
            raise ValueError("Cannot call encode method. TreeMutation requires encode method in Individual")
        except Exception as e:
            raise e

        return ret_indv
