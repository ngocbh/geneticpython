from __future__ import absolute_import

from geneticpython.utils.validation import check_random_state

from typing import Iterable
from copy import deepcopy

class rset():
    def __init__(self, l: Iterable=[]):
        self.__arr = list()
        self.__hashd = dict()
        self.__lastitem = None
        for x in l:
            self.add(x)

    def __contains__(self, x):
        index = self.__hashd.get(x, None)
        return (index is not None)

    def __iter__(self):
        return iter(self.__arr)

    def __len__(self):
        return len(self.__arr)

    def __repr__(self):
        ret = '{'
        for i, e in enumerate(self.__arr):
            ret += str(e) + (', ' if (i != len(self.__arr)-1) else '')
        ret += '}'
        return ret

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, key):
        if key < 0 or key >= len(self.__arr):
            raise IndexError('index({}) out of range'.format(key))
        return self.__arr[key]

    def add(self, x):
        if x in self.__hashd:
            return
    
        size = len(self.__arr)
        self.__arr.append(x)
        self.__hashd[x] = size
        self.__lastitem = x

    def remove(self, x):
        index = self.__hashd.get(x, None)
        if index is None:
            raise ValueError(f'{x} not in rset')
        # If present, then remove  
        # element from hash 
        self.__hashd.pop(x)

        # Swap element with last element  
        # so that removal from the list  
        # can be done in O(1) time 
        size = len(self.__arr)
        if index < size-1:
            last = self.__arr[size - 1]
            self.__arr[index], self.__arr[size-1] = \
                self.__arr[size-1], self.__arr[index]
            self.__hashd[last] = index

        # Remove last element (This is O(1))  
        self.__arr.pop()

    def discard(self, x):
        index = self.__hashd.get(x, None)
        if index is None:
            return
        self.remove(x)

    def pop(self, random_state=None):
        random_state = check_random_state(random_state)
        index = random_state.randint(0, len(self.__arr))
        self.remove(self.__arr[index])
        
    def clear(self):
        while len(self.__arr) > 0:
            self.pop()

    def update(self, t: Iterable):
        for x in t:
            self.add(x)

    def random_choice(self, random_state=None):
        random_state = check_random_state(random_state)
        index = random_state.randint(0, len(self.__arr))
        return self.__arr[index]

    def copy(self):
        return deepcopy(self)

    def hash_index(self):
        return self.__hashd

