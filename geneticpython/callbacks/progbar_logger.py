"""
File: progbar_logger.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

from __future__ import absolute_import

from collections import OrderedDict
from tqdm import tqdm
from typing import Union, Dict
from .callback import Callback


class ProgbarLogger(Callback):
    def __init__(self, metrics=None, default_metrics=True):
        self.metrics = metrics or {}
        self.default_metrics = default_metrics

    def on_init_population_begin(self, logs=None):
        print('Initializing...', flush=True)

    def on_init_population_end(self, logs=None):
        print('Finished Initialization!')
        print('Beginning genetic process...', flush=True)
        self.progbar = tqdm(range(self.engine.generations))

    def on_generation_end(self, gen, logs=None):
        self._update_metrics()
        self.progbar.set_postfix(self.metrics, refresh=True)
        self.progbar.update()

    def on_running_end(self, logs=None):
        self.progbar.close()
        print('Done!')

    def _update_metrics(self):
        self.metrics = self.metrics or OrderedDict()
        if self.default_metrics and self.engine.metrics:
            if not isinstance(self.engine.metrics, (dict, OrderedDict)):
                raise TypeError(
                    f'engine.metrics (type : {type(self.engine.metrics).__name__}) has be an instance of Dict or OrderedDict')
            self.metrics.update(self.engine.metrics)
