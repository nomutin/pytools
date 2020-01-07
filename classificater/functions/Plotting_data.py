import matplotlib.pyplot as plt
import numpy as np


class Plot:
    @staticmethod
    def linear_function(_a, _b, _x):
        """ indicate a linear function y = a + bx """
        x = np.linspace(_x.min(), _x.max())
        y = _a + _b * x
        plt.plot(x, y, "r-", label=f'y = {round(_a, 5)} + {round(_b, 5)} x')

    @staticmethod
    def two_dimensioned_data(_x, _y, _label):
        plt.plot(_x, _y, "o")

    @staticmethod
    def labeled_two_dimensioned_date(_x, _y, _label):
        for i in range(0, _x.shape[0]):
            if _label[i] == 1:
                plt.plot(_x[i], _y[i], 'ro')
            else:
                plt.plot(_x[i], _y[i], 'bo')

    @staticmethod
    def show():
        plt.legend(loc='best')
        plt.show()



