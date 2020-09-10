"""
File: pareto_metrics.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: This implementation bases on the following work:
T. Okabe, Y. Jin and B. Sendhoff, "A critical survey of performance indices for multi-objective optimisation," 
The 2003 Congress on Evolutionary Computation, 2003. 
CEC '03., Canberra, ACT, Australia, 2003, pp. 878-885 Vol.2, doi: 10.1109/CEC.2003.1299759. 
"""

from __future__ import absolute_import
from typing import Union
from geneticpython.core.population import SimplePareto, Pareto
from geneticpython.core.individual import SimpleSolution

from copy import deepcopy
import math
import numpy as np

def is_dominated(a: SimpleSolution, b: SimpleSolution) -> bool:
    """
        Return True if a dominate b, otherwise return False
    """
    if len(a) != len(b):
        msg = 'The length of objective in two solutions is not the same:\
             a has {} objectives, b has {} objectives'
        msg = msg.format(len(a), len(b))
        raise ValueError(msg)

    dominated = False
    for i in range(len(a)):
        if a[i] > b[i]:
            return False
        elif a[i] < b[i]:
            dominated = True

    return dominated

def euclidean_distance(a: SimpleSolution, b: SimpleSolution):
    """euclidean_distance.

    Args:
        a (SimpleSolution): a
        b (SimpleSolution): b
    """
    if len(a) != len(b):
        msg = 'The length of objective in two solutions is not the same:\
             a has {} objectives, b has {} objectives'
        msg = msg.format(len(a), len(b))
        raise ValueError(msg)
    d = 0
    for i in range(len(a)):
        d += (a[i] - b[i]) ** 2

    d = math.sqrt(d)
    return d
    
def l1_distance(a: SimpleSolution, b: SimpleSolution):
    if len(a) != len(b):
        msg = 'The length of objective in two solutions is not the same:\
             a has {} objectives, b has {} objectives'
        msg = msg.format(len(a), len(b))
        raise ValueError(msg)
    d = 0
    for i in range(len(a)):
        d += math.fabs(a[i] - b[i])

    return d

def delta_metric(S : Union[Pareto, SimplePareto]):
    """delta_metric.

    Args:
        A (Union[Pareto, SimplePareto]): A
    """
    if isinstance(S, Pareto):
        S = S.all_objectives()
    B = deepcopy(S)
    B.sort()
    n = len(B)
    d = np.zeros(n-1)
    for i in range(n-1):
        d[i] = euclidean_distance(B[i], B[i+1])

    d_mean = np.mean(d) 
    delta = np.sum(np.abs(d - d_mean)) / (n-1)
    return delta
 
def spacing_metric(S: Union[Pareto, SimplePareto]):
    if isinstance(S, Pareto):
        S = S.all_objectives()
    B = deepcopy(S)
    n = len(B)
    d = np.full(n, np.inf)
    for i in range(n):
        for j in range(n):
            if i != j:
                d[i] = min(d[i], l1_distance(B[i], B[j]))

    d_mean = np.mean(d)
    sp = np.sqrt(np.sum(np.square(d_mean - d)) / (n-1))
    return sp

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

def hypervolume_metric(S: SimplePareto, r : SimpleSolution):
    raise NotImplementedError

def non_dominated_solutions(S: Union[Pareto, SimplePareto]):
    if isinstance(S, Pareto):
        S = S.all_objectives()

    return len(S)
