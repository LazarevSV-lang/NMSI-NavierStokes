import numpy as np

def energy(u, v):
    return 0.5*np.mean(u*u + v*v)

def enstrophy(u, v):
    vx = np.roll(v, -1, axis=1) - np.roll(v, 1, axis=1)
    uy = np.roll(u, -1, axis=0) - np.roll(u, 1, axis=0)
    w  = vx - uy
    return np.mean(w*w)
