from __future__ import absolute_import

from geneticpython.utils.typing import SimplePareto, SimpleSolution
from typing import Union

import numpy as np
import random


def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance
    Parameters
    ----------
    seed : None, int or instance of RandomState
        If seed is None, return the RandomState singleton used by np.random.
        If seed is an int, return a new RandomState instance seeded with seed.
        If seed is already a RandomState instance, return it.
        Otherwise raise ValueError.
    """
    if seed is None or seed is np.random:
        return np.random.RandomState()
    if isinstance(seed, int):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState'
                     ' instance' % seed)

def check_simple_pareto(*args):
    """check_simple_pareto.
        Turn simple pareto into ndarry instance

    Args:
        S (Union[Pareto, SimplePareto]): S
    """
    ret = []
    for arg in args: 
        S: SimplePareto = arg
        if isinstance(S, np.ndarray):
            if S.ndim != 2:
                raise ValueError('SimplePareto in ndarray: has to be in 2-dimensional')
            if not np.issubdtype(S.dtype, np.integer) and not np.issubdtype(S.dtype, np.floating):
                raise ValueError('SimplePareto in ndarray: Invalid dtype')
            return S
        if len(S) == 0:
            return np.array(S)
        if any(len(s) != len(S[0]) for s in S):
            raise ValueError("SimplePareto in List: S donot have the consistent dimension")
        ret.append(np.array(S))
    if len(ret) == 1:
        return ret[0]
    else:
        return (*ret, )

def check_simple_solution(*args):
    ret = []
    for arg in args: 
        s: SimpleSolution = arg
        if isinstance(s, np.ndarray):
            if s.ndim != 1:
                raise ValueError('SimplePareto in ndarray: has to be in 1-dimensional')
            if not np.issubdtype(s.dtype, np.integer) and not np.issubdtype(s.dtype, np.floating):
                raise ValueError('SimplePareto in ndarray: Invalid dtype')
            ret.append(s)
        else:
            ret.append(np.array(s))
    if len(ret) == 1:
        return ret[0]
    else:
        return (*ret, )

