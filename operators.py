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

def pi_star_factor(t, A_pi=0.15, omega_pi=3.5):
    return A_pi * np.sin(omega_pi * t)

def pi_star_term(u, t, A_pi=0.15, omega_pi=3.5):
    fac = pi_star_factor(t, A_pi, omega_pi)
    if isinstance(u, (list, tuple)):
        return [fac * ui for ui in u]
    return fac * u

def pi_star_term_with_shape(f, t, A_pi=0.15, omega_pi=3.5):
    return pi_star_factor(t, A_pi, omega_pi) * f
