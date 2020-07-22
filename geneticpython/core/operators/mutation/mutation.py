"""
# Problem: mutation.py
# Description: 
# Created by ngocjr7 on [2020-03-31 14:53:16]
"""
from __future__ import absolute_import
from abc import ABC, abstractmethod

class Mutation:
    def __init__(self):
        pass

    @abstractmethod
    def mutate(self):
        raise NotImplementedError