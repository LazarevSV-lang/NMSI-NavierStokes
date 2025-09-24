import numpy as np

def e_operator_factor(t, lam_e=0.6, alpha_e=0.25):
    return -lam_e * np.exp(-alpha_e * t)

def e_term_physical(u, t, lam_e=0.6, alpha_e=0.25):
    fac = e_operator_factor(t, lam_e, alpha_e)
    if isinstance(u, (list, tuple)):
        return [fac * ui for ui in u]
    return fac * u

def e_term_spectral(u_hat, t, lam_e=0.6, alpha_e=0.25):
    fac = e_operator_factor(t, lam_e, alpha_e)
    if isinstance(u_hat, (list, tuple)):
        return [fac * uh for uh in u_hat]
    return fac * u_hat
