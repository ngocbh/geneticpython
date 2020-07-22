"""
# Problem: crossover.py
# Description: 
# Created by ngocjr7 on [2020-03-31 14:54:08]
"""
from __future__ import absolute_import
from abc import ABC, abstractmethod

class Crossover:
    def __init__(self):
        pass

    @abstractmethod
    def cross(self):
        raise NotImplementedError