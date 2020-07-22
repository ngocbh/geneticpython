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

    def on_init_population_end(self, logs=None):
        self.progbar = tqdm(range(self.engine.MAX_ITER))

    def on_generation_end(self, gen, logs=None):
        logs = self._update_logs(logs)
        self.progbar.set_postfix(logs, refresh=True)
        self.progbar.update()

    def on_running_end(self, logs=None):
        self.progbar.close()

    def _update_logs(self, logs):
        logs = logs or OrderedDict()
        if self.default_metrics and self.engine.metrics:
            if not isinstance(self.engine.metrics, (dict, OrderedDict)):
                raise TypeError(
                    f'engine.metrics (type : {type(self.engine.metrics).__name__}) has be an instance of Dict or OrderedDict')
            for name, value in self.engine.metrics.items():
                logs[name] = value

        return logs
