"""
# Problem: gene.py
# Description: 
# Created by ngocjr7 on [2020-03-29 22:09:48]
"""
from __future__ import absolute_import

import random

class Gene:
    """
        domain is list of value that this gene can be
    """
    vtype = 'int'

    def __init__(self, min_value, max_value, value=0):
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    
    @staticmethod
    def set_type(vtype):
        Gene.vtype = vtype
        
    def set_random_value(self, rand=None):
        if not rand:
            rand = random.Random()
        if Gene.vtype == 'int':
            self.value = rand.randint(self.min_value,self.max_value)        
        elif Gene.vtype == 'float':
            self.value = rand.uniform(self.min_value,self.max_value)
    
    @property
    def is_valid(self):
        if not self.value:
            return False
        if self.min_value <= self.value and self.value <= self.max_value:
            return True
        return False