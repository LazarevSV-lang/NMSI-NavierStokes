import numpy as np

def energy(u):
    return 0.5*np.mean((u**2).sum(-1))

def vorticity(u):
    # Placeholder: requires finite diff implementation
    return np.zeros_like(u)

def enstrophy(u):
    return np.mean((vorticity(u)**2).sum(-1))

def wmax(u):
    return np.abs(vorticity(u)).max()
