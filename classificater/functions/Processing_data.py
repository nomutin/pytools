import numpy as np


class TwoDimensionedData(object):
    def __init__(self, path_to_tsv_data_file, labelled=False):
        with open(path_to_tsv_data_file, 'r') as file:
            self._data = np.array([[float(i) for i in line.split()] for line in file.readlines()])
        self._x = self._data[:, 0]
        self._y = self._data[:, 1]
        if labelled:
            self._label = self._data[:, 2]

    def data(self): return self._data

    def x(self): return self._x

    def y(self): return self._y

    def x_ones(self):
        return np.c_[np.ones(self._x.size).T, self._x]

    def label(self): return self._label

