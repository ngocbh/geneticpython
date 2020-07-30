"""
File: pareto_metrics.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

from __future__ import absolute_import
from typing import Union
from geneticpython.core.population import SimplePareto, Pareto
from geneticpython.core.individual import SimpleSolution

def is_dominated(a: SimpleSolution, b: SimpleSolution) -> bool:
    """
        Return True if a dominate b, otherwise return False
    """
    if len(a._objectives) != len(b._objectives):
        msg = 'The length of objective in two solutions is not the same:\
             a has {} objectives, b has {} objectives'
        msg = msg.format(len(a._objectives), len(b._objectives))
        raise ValueError(msg)

    dominated = False
    for i in range(len(a._objectives)):
        if a[i] > b[i]:
            return False
        elif a[i] < b[i]:
            dominated = True

    return dominated

def coverage_metric(A : Union[Pareto, SimplePareto], B : Union[Pareto, SimplePareto]):
    if isinstance(A, Pareto):
        A = A.all_objectives()
    if isinstance(B, Pareto):
        B = B.all_objectives()

    noadb = 0
    for x in B:
        if any(is_dominated(y, x) for y in A):
            noadb += 1

    return noadb / len(B)

def non_dominated_solutions(A: Union[Pareto, SimplePareto]):
    if isinstance(Pareto):
        A = A.all_objectives()

    return len(A)
