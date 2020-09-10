"""
# Problem: crossover.py
# Description: 
# Created by ngocjr7 on [2020-03-31 14:54:08]
"""
from __future__ import absolute_import
from abc import ABC, abstractmethod
from typing import Tuple

from geneticpython.core.individual import Individual

class Crossover:
    def __init__(self, pc : float):
        if pc < 0.0 or pc > 1.0:
            raise ValueError('Invalid crossover probability')
        self.pc = pc

    @abstractmethod
    def cross(self, father : Individual, mother : Individual, random_state=None) -> Tuple[Individual]:
        raise NotImplementedError
