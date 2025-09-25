import numpy as np

def e_operator(u, lam=0.4, alpha=0.2):
    return u*np.exp(-lam*np.abs(u)**alpha)
