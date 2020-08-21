import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from math import sqrt, pi


def normal_distribution(_loc, _scale, sigma=5, x_interval=1, max_height=1):
    _start = _loc - _scale * sigma
    _end = _loc + _scale * sigma
    _x = np.arange(_start, _end, x_interval)
    return _x, norm.pdf(_x, loc=_loc, scale=_scale) * sqrt(2 * pi) * _scale * max_height


def spectrum(func='scatter'):
    vs_min, vs_max = 380, 800
    locs = (700, 546, 436)

    plt.xlim(vs_min, vs_max)

    rx, ry = normal_distribution(locs[0], 90, max_height=255)
    gx, gy = normal_distribution(locs[1], 90, max_height=255)
    bx, by = normal_distribution(locs[2], 90, max_height=255)

    r = [[k, l] for k, l in zip(rx, ry)]
    g = [[k, l] for k, l in zip(gx, gy)]
    b = [[k, l] for k, l in zip(bx, by)]

    colors = []
    for i in range(vs_min, vs_max):
        ps = '#'

        rl = [hex(int(k[1]))[2:].zfill(2) for k in r if k[0] == i]
        ps += '00' if rl is None else rl[0]

        gl = [hex(int(k[1]))[2:].zfill(2) for k in g if k[0] == i]
        ps += '00' if gl is None else gl[0]

        bl = [hex(int(k[1]))[2:].zfill(2) for k in b if k[0] == i]
        ps += '00' if bl is None else bl[0]

        colors.append(ps)

    if func == 'scatter':
        plt.grid(color='gray')
        plt.plot(rx, ry, color='red')
        plt.plot(gx, gy, color='green')
        plt.plot(bx, by, color='blue')

    else:
        plt.bar(np.arange(vs_min, vs_max, 1), [1 for _ in range(vs_min, vs_max)], color=colors, width=1)

    plt.show()


if __name__ == '__main__':
    spectrum(func='')
