
from typing import List, Union, Callable, Tuple, NewType

import numpy as np


SimpleSolution = NewType("SimpleSolution", Union[ List[Union[int, float]], Tuple[Union[int, float]], np.ndarray])
SimplePareto = NewType('SimplePareto', Union[List[SimpleSolution], Tuple[SimpleSolution], np.ndarray])
