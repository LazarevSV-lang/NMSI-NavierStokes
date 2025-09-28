import numpy as np
from scipy.signal import stft

def cairo_residual(x, fs=1.0):
    f, t, Zxx = stft(x, fs=fs)
    res = np.var(np.abs(Zxx), axis=0)
    return f, t, res
