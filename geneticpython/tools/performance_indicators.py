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
from geneticpython.core.pareto import Pareto
from geneticpython.utils.typing import SimplePareto, SimpleSolution
from geneticpython.tools.math import is_dominated, l1_distance, euclidean_distance
from geneticpython.utils.validation import check_simple_pareto, check_simple_solution

from copy import deepcopy
import math
import numpy as np


def check_pareto(*args):
    ret = []
    for arg in args:
        S: Union[Pareto, SimplePareto] = arg
        if isinstance(S, Pareto):
            S = S.all_objectives()
        ret.append(check_simple_pareto(S))
    if len(ret) == 1:
        return ret[0]
    else:
        return (*ret, )

"""
========================================================================
this section includes the performance indicators which do not require
referenced pareto (The true pareto)
========================================================================
"""


def delta_apostrophe(S: Union[Pareto, SimplePareto]):
    """delta_metric.
        delta'

        Aspect: Diversity
        Sets: Unary
    Args:
        A (Union[Pareto, SimplePareto]): A
    """
    S = check_pareto(S)
    S = S[np.lexsort(np.rot90(S))]
    n = len(S)
    if n < 2:
        return float('inf') 

    d = np.zeros(n-1)
    for i in range(n-1):
        d[i] = euclidean_distance(S[i], S[i+1])

    d_mean = np.mean(d)
    delta = np.sum(np.abs(d - d_mean)) / (n-1)

    return delta


def spacing(S: Union[Pareto, SimplePareto]):
    """spacing.
        Aspect: Diverity
        Sets: Unary

    Args:
        S (Union[Pareto, SimplePareto]): S
    """
    S = check_pareto(S)
    n = len(S)
    d = np.full(n, np.inf)
    for i in range(n):
        for j in range(n):
            if i != j:
                d[i] = min(d[i], l1_distance(S[i], S[j]))

    if n < 2:
        return float('inf')

    d_mean = np.mean(d)
    sp = np.sqrt(np.sum(np.square(d_mean - d)) / (n-1))
    return sp


def two_sets_coverage(A: Union[Pareto, SimplePareto], B: Union[Pareto, SimplePareto]):
    """coverage.
        Aspect: All (Diversity, Accuracy, Cardinality)
        Sets: Binary

    Args:
        A (Union[Pareto, SimplePareto]): A
        B (Union[Pareto, SimplePareto]): B
    """
    A, B = check_pareto(A, B)

    noadb = 0
    for x in B:
        if any(is_dominated(y, x) for y in A):
            noadb += 1

    return noadb / len(B)


def hypervolume_2d(S: Union[Pareto, SimplePareto], r: SimpleSolution):
    """hypervolume_2d.
        http://www.mathwords.com/a/area_convex_polygon.htm
        Aspect: Accuracy and Diversity
        Sets: Unary

    Args:
        S (SimplePareto): S
        r (SimpleSolution): r
    """
    S = check_pareto(S)
    r = check_simple_solution(r)
    if S.shape[1] != 2 or len(r) != 2:
        raise ValueError(
            'This implementation is only used for 2-dimensional space')
    n = len(S)
    if n == 0:
        return 0

    S = S[np.lexsort(np.rot90(S))]
    S = S.astype(np.float64)
    r = r.astype(np.float64)
    r_temp = np.copy(r)
    HV = 0
    for i in range(n):
        # print(i, S[i], r_temp)
        # print(np.abs(r_temp[0] - S[i][0]) * np.abs(r_temp[1] - S[i][1]))
        HV += np.abs(r_temp[0] - S[i][0]) * np.abs(r_temp[1] - S[i][1])
        r_temp[1] = S[i][1]
        # print(r_temp, S[i][1])

    # print (S, r, HV)
    # print(HV)
    return HV


def hypervolume(S: SimplePareto, r: SimpleSolution):
    """hypervolume.
        Aspect: Accuracy and Diversity
        Sets: Unary

        2006 IEEE Congress on Evolutionary Computation
        Carlos M. Fonseca, An Improved Dimension-Sweep Algorithm for the Hypervolume Indicator

    Args:
        S (SimplePareto): S
        r (SimpleSolution): r
    """
    S = check_pareto(S)
    r = check_simple_solution(r)
    raise NotImplementedError


def overall_non_dominated_vector_generation(S: Union[Pareto, SimplePareto]):
    """non_dominated_solutions.
        Aspect: Cardinality
        Sets: Unary

    Args:
        S (Union[Pareto, SimplePareto]): S
    """
    S = check_pareto(S)

    return len(S)


"""
========================================================================
this section includes the performance indicators which do not require
referenced pareto (The true pareto)
========================================================================
"""


def delta(S: Union[Pareto, SimplePareto], P: Union[Pareto, SimplePareto]):
    """delta.

    Args:
        S (Union[Pareto, SimplePareto]): S
        P (Union[Pareto, SimplePareto]): P
    """
    S, P = check_pareto(S, P)
    S = S[np.lexsort(np.rot90(S))]
    P = P[np.lexsort(np.rot90(P))]
    n = len(S)
    if n < 2:
        return 1.0 

    d = np.zeros(n-1)
    for i in range(n-1):
        d[i] = euclidean_distance(S[i], S[i+1])

    df = euclidean_distance(S[0], P[0])
    dl = euclidean_distance(S[-1], P[-1])

    d_mean = np.mean(d)
    delta = (df + dl + np.sum(np.abs(d - d_mean))) /( df + dl + (n-1) * d_mean)

    return delta


def delta_star(S: Union[Pareto, SimplePareto], P: Union[Pareto, SimplePareto]):
    """delta_star.

    Args:
        S (Union[Pareto, SimplePareto]): S
        P (Union[Pareto, SimplePareto]): P
    """
    S, P = check_pareto(S, P)
    raise NotImplementedError


def generational_distance(S: Union[Pareto, SimplePareto], P: Union[Pareto, SimplePareto], p=2):
    """generational_distance.

    Args:
        S (Union[Pareto, SimplePareto]): S
        P (Union[Pareto, SimplePareto]): P
        p:
    """
    S, P = check_pareto(S, P)
    n = len(S)
    GD = 0
    for s in S:
        i = np.argmin(np.linalg.norm(s - P, axis=1))
        # print(s, i, P[i])
        GD += np.min(np.linalg.norm(s - P, axis=1))**p
    GD = np.power(GD, 1/p) / n
    return GD

def inverted_generational_distance(S: Union[Pareto, SimplePareto], P: Union[Pareto, SimplePareto], p=2):
    """inverted_generational_distance.

    Args:
        S (Union[Pareto, SimplePareto]): S
        P (Union[Pareto, SimplePareto]): P
        p:
    """
    S, P = check_pareto(S, P)
    n = len(P)
    IGD = 0
    for _p in P:
        i = np.argmin(np.linalg.norm(S - _p, axis=1))
        IGD += np.min(np.linalg.norm(S - _p, axis=1))**p
    IGD = np.power(IGD, 1/p) / n
    return IGD

"""
=======================================================================
Short name of the metrics
=======================================================================
"""
SP = spacing
C_metric = two_sets_coverage
HV_2d = hypervolume_2d
HV = hypervolume
ONVG = overall_non_dominated_vector_generation
GD = generational_distance
IGD = inverted_generational_distance
