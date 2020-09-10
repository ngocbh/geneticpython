"""
# Problem: mutation.py
# Description: 
# Created by ngocjr7 on [2020-03-31 14:53:16]
"""
from __future__ import absolute_import
from abc import ABC, abstractmethod
from geneticpython.core.individual import Individual

class Mutation:
    def __init__(self, pm : float):
        if pm < 0.0 or pm > 1.0:
            raise ValueError('Invalid mutation probability')
        self.pm = pm

    @abstractmethod
    def mutate(self, indv : Individual, random_state=None) -> Individual:
        raise NotImplementedError
