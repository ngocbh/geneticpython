from __future__ import absolute_import

import re, numpy as np


class DemsInput:
    def __init__(self, _cols, _rows, _cellsize, _height):
        self.cols = _cols
        self.rows = _rows
        self.cellsize = _cellsize
        self.height = _height

    def scale(self, new_cols, new_rows, new_cellsize = None):
        self.cols = new_cols
        self.rows = new_rows
        if new_cellsize is None:
            new_cellsize = self.cellsize
        self.cellsize = new_cellsize
        self.height = self.height[:new_rows, :new_cols]

    @classmethod
    def from_file(cls, path):
        f = open(path, "r")
        cols = int(f.readline().strip().split(' ')[1])
        rows = int(f.readline().strip().split(' ')[1])
        xllcorner = float(f.readline().strip().split(' ')[1])
        yllcorner = float(f.readline().strip().split(' ')[1])
        cellsize = int(f.readline().strip().split(' ')[1])
        NODATA_VALUE = int(f.readline().strip().split(' ')[1])
        height = np.zeros([rows, cols], dtype=float)
        # height = [[0]*cols]*rows
        for i in range(rows):
            row = re.sub(' +', ' ', f.readline()).strip().split(' ')
            for j in range(cols):
                height[i][j] = row[j]
        f.close()
        return DemsInput(cols, rows, cellsize, height)