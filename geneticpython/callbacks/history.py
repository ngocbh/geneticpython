"""
File: history.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

from __future__ import absolute_import

import os

from .callback import Callback


class History(Callback):
    def __init__(self):
        pass

    def on_init_population_end(self, logs=None):
        pass

    def on_generation_begin(self, gen, logs=None):
        pass

    def on_generation_end(self, gen, logs=None):
        pass


class MultiObjectiveHistory(History):
    pass


class SingleObjectiveHistory(History):
    pass
