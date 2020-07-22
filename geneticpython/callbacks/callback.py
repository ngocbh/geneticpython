"""
File: callback.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

from __future__ import absolute_import

from abc import ABC, abstractmethod
from typing import List
import os


class Callback(object):
    def __init__(self):
        pass

    def set_engine(self, engine):
        self.engine = engine

    def set_params(self, params):
        self.params = params

    def on_running_begin(self, logs=None):
        pass

    def on_running_end(self, logs=None):
        pass

    def on_init_population_begin(self, logs=None):
        pass

    def on_init_population_end(self, logs=None):
        pass

    def on_generation_begin(self, gen, logs=None):
        pass

    def on_generation_end(self, gen, logs=None):
        pass

    def on_selection_begin(self, gen, logs=None):
        pass

    def on_selection_end(self, gen, logs=None):
        pass

    def on_reproduction_begin(self, gen, logs=None):
        pass

    def on_reproduction_end(self, gen, logs=None):
        pass

    def on_evaluation_begin(self, gen, logs=None):
        pass

    def on_evaluation_end(self, gen, logs=None):
        pass

    def on_replacement_begin(self, gen, logs=None):
        pass

    def on_replacement_end(self, gen, logs=None):
        pass
