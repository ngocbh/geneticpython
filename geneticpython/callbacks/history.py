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
import copy
import json

class History(Callback):
    """Callback that records events into a `History` object.
    This callback is automatically applied to
    every Genetic engine. The `History` object
    gets returned by the `run` method of engine.
    """

    def __init__(self):
        super(History, self).__init__()
        self.history = []

    def on_init_population_end(self, logs=None):
        logs = logs or {}
        self.history.append(copy.deepcopy(logs))
        # Set the history attribute on the model after the epoch ends. This will
        # make sure that the state which is set is the latest one.
        self.engine.history = self

    def on_generation_begin(self, gen, logs=None):
        pass

    def on_generation_end(self, gen, logs=None):
        logs = logs or {}
        self.history.append(copy.deepcopy(logs))
        # Set the history attribute on the model after the epoch ends. This will
        # make sure that the state which is set is the latest one.
        self.engine.history = self

    def dump(self, filepath):
        with open(filepath, mode='w') as f:
            history_json = json.dumps(self.history, indent=2)
            f.write(history_json)

