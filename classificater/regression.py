# -*- coding: utf-8 -*-


def h(x_i, theta):
    return x_i @ theta.T


def costFunctionJ(_x, _y, _theta):
    m = _x.shape[0]
    summation = 0
    for i in range(0, m):
        summation += (h(_x[i, :], _theta) - _y[i])**2
    return 1 / 2 / m * summation
