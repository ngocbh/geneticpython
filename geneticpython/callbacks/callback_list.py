"""
File: callback_list.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

from __future__ import absolute_import

from typing import List

from .callback import Callback
from .history import History
from .progbar_logger import ProgbarLogger


class CallbackList():
    def __init__(self, callbacks: List[Callback] = None, add_history=False, add_progbar=False):
        self.callbacks = callbacks if callbacks else []
        self._add_default_callbacks(
            add_history, add_progbar)

    def _add_default_callbacks(self, add_history, add_progbar):
        self._history = None
        self._progbar = None

        for cb in self.callbacks:
            if isinstance(cb, History) and add_history:
                self._history = cb
            elif isinstance(cb, ProgbarLogger):
                self._progbar = cb

        if self._history is None and add_history:
            self._history = History()
            self.callbacks.append(self._history)
        if self._progbar is None and add_progbar:
            self._progbar = ProgbarLogger()
            self.callbacks.append(self._progbar)

    def append(self, callback):
        self.callbacks.append(callback)

    def set_params(self, params):
        self.params = params
        for callback in self.callbacks:
            callback.set_params(params)

    def set_engine(self, engine):
        self.engine = engine

        for callback in self.callbacks:
            callback.set_engine(engine)

    def on_running_begin(self, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_running_begin(logs)

    def on_running_end(self, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_running_end(logs)

    def on_init_population_begin(self, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_init_population_begin(logs)

    def on_init_population_end(self, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_init_population_end(logs)

    def on_generation_begin(self, gen, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_generation_begin(gen, logs)

    def on_generation_end(self, gen, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_generation_end(gen, logs)

    def on_reproduction_begin(self, gen, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_reproduction_begin(gen, logs)

    def on_reproduction_end(self, gen, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_reproduction_end(gen, logs)

    def on_evaluation_begin(self, gen, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_evaluation_begin(gen, logs)

    def on_evaluation_end(self, gen, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_evaluation_end(gen, logs)

    def on_selection_begin(self, gen, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_selection_begin(gen, logs)

    def on_selection_end(self, gen, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_selection_end(gen, logs)

    def on_replacement_begin(self, gen, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_replacement_begin(gen, logs)

    def on_replacement_end(self, gen, logs=None):
        logs = logs or {}

        for callback in self.callbacks:
            callback.on_replacement_end(gen, logs)
