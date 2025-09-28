import numpy as np

def twoflow_step(u1, u2, dt, params):
    pi_star, gamma_diss, e_star = params
    du1 = -pi_star*u1 + gamma_diss*u2 + e_star
    du2 = -pi_star*u2 + gamma_diss*u1 - e_star
    return u1+dt*du1, u2+dt*du2
