"""
# Filename: replacement.py
# Description:
# Created by ngocjr7 on [07-06-2020 00:52:40]
"""
from __future__ import absolute_import

from geneticpython.core.individual import Individual

from abc import ABC, abstractmethod
from typing import List

class Replacement:
    def __init__(self):
        pass
    
    @abstractmethod
    def replace(self, size : int, population : List[Individual], random_state=None):
        raise NotImplementedError
