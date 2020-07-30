"""
# Problem: solution.py
# Description: 
# Created by ngocjr7 on [2020-03-29 20:29:20]
"""
from __future__ import absolute_import

from typing import List, Union, Callable, Tuple, NewType

SimpleSolution = NewType("SimpleSolution", Union[ List[Union[int, float]], Tuple[Union[int, float]] ])

class Solution:
    def __init__(self):
        pass
    
    @property
    def is_valid(self):
        """
            check if this solution is valid
        :return true if valid
        :rtype boolean
        """
        raise NotImplementedError
