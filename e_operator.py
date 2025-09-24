import numpy as np

def e_operator_factor(t, lam_e=0.6, alpha_e=0.25):
    """
    Scalar multiplier for the exponential stabilizer:
        e(u) = -lam_e * exp(-alpha_e * t) * u
    """
    return -lam_e * np.exp(-alpha_e * t)

def e_term_physical(u, t, lam_e=0.6, alpha_e=0.25):
    """
    Apply e-operator in physical space to a field u (array or list/tuple of arrays).
    """
    fac = e_operator_factor(t, lam_e, alpha_e)
    if isinstance(u, (list, tuple)):
        return [fac * ui for ui in u]
    return fac * u

def e_term_spectral(u_hat, t, lam_e=0.6, alpha_e=0.25):
    """
    Apply e-operator in spectral space to Fourier coefficients u_hat.
    """
    fac = e_operator_factor(t, lam_e, alpha_e)
    if isinstance(u_hat, (list, tuple)):
        return [fac * uh for uh in u_hat]
    return fac * u_hat
