import numpy as np

def energy_decay(E0, t, beta=0.03):
    return E0 * np.exp(-beta*t)

def enstrophy_bound(Omega0, t, gamma=0.06):
    return Omega0 * (0.6 + 0.4*np.exp(-gamma*t))

def spectra_k(k, alpha=5/3):
    k = np.asarray(k)
    return np.maximum(k,1.0)**(-alpha)
