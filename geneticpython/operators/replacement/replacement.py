"""
# Filename: replacement.py
# Description:
# Created by ngocjr7 on [07-06-2020 00:52:40]
"""
from __future__ import absolute_import
from abc import ABC, abstractmethod

class Replacement:
    def __init__(self):
        pass
    
    @abstractmethod
    def replace(self):
        raise NotImplementedError