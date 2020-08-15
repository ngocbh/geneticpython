"""
File: prufer.py
Created by ngocjr7 on 2020-08-15 21:44
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""
from __future__ import absolute_import

from geneticpython.core.individual import Individual
from geneticpython.core.individual.chromosome import IntChromosome

from .tree import Tree

class Prufer(Individual):
    def __init__(self):
        pass

    def decode(self):
        pass

    @classmethod
    def encode(cls, tree : Tree):
        pass
