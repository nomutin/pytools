import numpy as np
from scipy.interpolate import interp1d


def spline_interp(in_theta, in_r):
    out_theta = np.linspace(np.min(in_theta), np.max(in_theta), np.size(in_theta)*100)
    func_spline = interp1d(in_theta, in_r, kind='cubic')
    out_r = func_spline(out_theta)
    return out_theta, out_r
