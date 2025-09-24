# Example of augmenting a Navier–Stokes spectral RHS with π* and e terms
import numpy as np
from operators import e_operator_factor, pi_star_factor

def augmented_rhs(u_hat, v_hat, Nu_hat, Nv_hat, visc_u, visc_v, t,
                  lam_e=0.6, alpha_e=0.25, A_pi=0.15, omega_pi=3.5):
    aug_e  = e_operator_factor(t, lam_e, alpha_e)
    aug_pi = pi_star_factor(t, A_pi, omega_pi)
    Ru_hat = Nu_hat + visc_u + (aug_pi + aug_e) * u_hat
    Rv_hat = Nv_hat + visc_v + (aug_pi + aug_e) * v_hat
    return Ru_hat, Rv_hat
