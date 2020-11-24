"""
File: prufer.py
Created by ngocjr7 on 2020-08-15 21:44
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: this implementation follows this tutorial: https://cp-algorithms.com/graph/pruefer_code.html
"""
from __future__ import absolute_import

from geneticpython.core.individual.chromosome import IntChromosome
from geneticpython.core.individual import Individual
from geneticpython.models.tree.tree import Tree
from geneticpython.models.int_individual import IntIndividual
from copy import deepcopy

class PruferCode(Individual):
    """PruferCode.
        the implementation follows tutorial: https://cp-algorithms.com/graph/pruefer_code.html
    """

    def __init__(self, number_of_vertices: int, chromosome: IntChromosome = None, solution: Tree = None):
        self.number_of_vertices = number_of_vertices
        solution = solution or Tree(number_of_vertices)
        chromosome = chromosome or IntChromosome(number_of_vertices-2, [0, number_of_vertices-1])

        super(PruferCode, self).__init__(chromosome=chromosome, solution=solution)

        if self.number_of_vertices != self.solution.number_of_vertices:
            raise ValueError('number_of_vertices is conflict in argument and solution')


    def clone(self):
        number_of_vertices = self.number_of_vertices
        solution = self.solution.clone()
        chromosome = deepcopy(self.chromosome)

        return PruferCode(number_of_vertices, chromosome=chromosome, solution=solution)

    def decode(self):
        """decode.
            Decode prufer code to Tree in linear time O(n)
        """
        n = self.number_of_vertices
        code = self.chromosome.genes
        degree = [1] * n
        for i in code:
            degree[i] += 1

        ptr = 0
        while degree[ptr] != 1:
            ptr += 1

        leaf = ptr
        edges = []
        for v in code:
            edges.append((leaf, v))
            degree[v] -= 1
            if degree[v] == 1 and v < ptr:
                leaf = v
            else:
                ptr += 1
                while degree[ptr] != 1:
                    ptr += 1
                leaf = ptr

        edges.append((leaf, n-1))

        self.solution.initialize()
        _is_valid = True
        for u, v in edges:
            _is_valid &= self.solution.add_edge(u, v)

        self.solution._is_valid = _is_valid
        self.solution.repair()
        return self.solution

    def encode(self, solution: Tree):
        """encode.
            Encode a Tree to prufer code in linear time O(n)

        Args:
            tree (Tree): tree
        """
        n = self.number_of_vertices
        parent = [-1] * n
        
        def dfs(adj, u):
            for v in adj[u]:
                if v != parent[u]:
                    parent[v] = u
                    dfs(adj, v)
        
        adj = solution.get_adjacency()
        dfs(adj, n-1)
        ptr = -1
        degree = [0] * n
        for i in range(n):
            degree[i] = len(adj[i])
            if degree[i] == 1 and ptr == -1:
                ptr = i

        genes = [0] * (n-2)
        leaf = ptr
        for i in range(n-2):
            _next = parent[leaf]
            genes[i] = _next
            degree[_next] -= 1
            if degree[_next] == 1 and _next < ptr:
                leaf = _next
            else:
                ptr += 1
                while degree[ptr] != 1:
                    ptr += 1
                leaf = ptr

        self.update_genes(genes)
        self.solution = solution
