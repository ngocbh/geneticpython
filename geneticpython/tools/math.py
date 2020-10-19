from geneticpython.utils.typing import SimpleSolution
from geneticpython.utils.validation import check_simple_solution

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
    a, b = check_simple_solution(a, b)

    return np.linalg.norm(a - b)
    
    
def l1_distance(a: SimpleSolution, b: SimpleSolution):
    if len(a) != len(b):
        msg = 'The length of objective in two solutions is not the same:\
             a has {} objectives, b has {} objectives'
        msg = msg.format(len(a), len(b))
        raise ValueError(msg)
    a, b = check_simple_solution(a, b)

    return np.linalg.norm(a - b, ord=1)
