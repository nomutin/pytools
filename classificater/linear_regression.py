import numpy as np

from functions.Processing_data import TwoDimensionedData
from functions.Plotting_data import Plot


def h(x_i, theta):
    return x_i @ theta.T


def CostFunctionJ(_x, _y, _theta):
    m = _x.shape[0]
    summation = 0
    for i in range(0, m):
        summation += (h(_x[i, :], _theta) - _y[i])**2
    return 1 / 2 / m * summation


class GradientDecent:
    """ only linear function, not polynomial function .                            """
    """ this function based on my definition of hypothesis function h() = X @ θ.T  """
    """ variable m is number of detaset, n is number of feature.                   """
    """ therefore, X is m*(n+1), θ is 1*(n+1) dimensioned matrix.                  """

    def __init__(self, _x, _y, _rate):
        self._x = _x
        self._y = _y
        self._rate = _rate
        self.theta = np.zeros((1, self._x.shape[1]))

    def gradient_decent(self):
        x, y = self._x, self._y
        m, n = self._x.shape[0], self._x.shape[1]
        for j in range(0, n):
            summation = sum([(h(x[i, :], self.theta) - y[i]) * x[i, j] for i in range(0, m)])
            self.theta[:, j] = self.theta[:, j] - self._rate * summation / m


def normal_equation(_x, _y):
    return np.linalg.inv(_x.T @ _x) @ _x.T @ _y


def normal_equation_method():
    data = TwoDimensionedData('cousera-1')
    theta = normal_equation(data.x_ones(), data.y())
    Plot.linear_function(theta[0], theta[1], data.x())
    Plot.two_dimensioned_data(data.x(), data.y())
    Plot.show()


def gradient_decent_method():
    data = TwoDimensionedData('cousera-1')
    gd = GradientDecent(data.x_ones(), data.y(), 0.02)
    for _ in range(1, 200):
        gd.gradient_decent()
        print(CostFunctionJ(data.x_ones(), data.y(), gd.theta))
    print(gd.theta)


if __name__ == '__main__':
    gradient_decent_method()
