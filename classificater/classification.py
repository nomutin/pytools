# -*- coding: utf-8 -*-
from math import log, exp
import numpy as np


def g(_z):
    return 1 / (1 + exp(_z))


def h(_theta, _x):
    return g(_x @ _theta.T)


def cost(_theta, _x, _y):
    return -1 * _y * log(h(_theta, _x)) - (1 - _y) * log(1 - h(_theta, _x))


class GradientDecent(object):
    def __init__(self, _x, _y, _rate):
        self._x = _x
        self._y = _y
        self._rate = _rate
        self._theta = np.zeros((_x.shape[0], 1))

    def gradient_decent(self, show_progress=True):
        print(self._x.shape)
        x, y = self._x, self._y
        m, n = self._x.shape[0], self._x.shape[1]
        for j in range(0, n):
            summation = sum([(h(self._theta, x[i, :]) - y[i]) * x[i, j] for i in range(0, m)])
            self._theta[:, j] = self._theta[:, j] - self._rate * summation / m
            if show_progress:
                print(self._theta)


if __name__ == '__main__':
    from functions.Processing_data import TwoDimensionedData
    from functions.Plotting_data import Plot
    data = TwoDimensionedData('data/cousera-2-1', labelled=True)
    gd = GradientDecent(data.x_ones(), data.y(), 0.02)
    gd.gradient_decent(show_progress=True)
    Plot.labeled_two_dimensioned_date(data.x(), data.y(), data.label())
    Plot.show()

