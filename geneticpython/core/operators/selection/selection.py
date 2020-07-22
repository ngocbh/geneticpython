"""
# Problem: selection.py
# Description: 
# Created by ngocjr7 on [2020-03-31 14:52:26]
"""
from __future__ import absolute_import
from abc import ABC, abstractmethod

class Selection:
    def __init__(self):
        pass
    
    @abstractmethod
    def select(self):
        raise NotImplementedError