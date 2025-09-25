import numpy as np

def Z_window(kmag, kmin, kmax):
    return (kmag>=kmin) & (kmag<=kmax)

def step(u, t, dt, fft, ifft, nonlinear_term, k_magnitude_grid, project_div_free,
         nu=1e-3, A_pi=0.2, omega_pi=2.0, phi=0.0, lam_e=0.4, alpha_e=0.2, gamma0=0.6, kmax=lambda: 1.0):
    û = fft(u)
    kmag = k_magnitude_grid(û.shape[:-1])
    NL  = nonlinear_term(u)
    ûNL = fft(NL)
    ûvis= - (nu * kmag**2)[:, :, :, None] * û

    Fpi = A_pi * np.sin(omega_pi*t + phi) * u
    ûF  = fft(Fpi)

    Z   = Z_window(kmag, kmin=0.6*kmax(), kmax=0.9*kmax()).astype(float)
    ûD  = - (gamma0 * Z)[:, :, :, None] * û

    ûE  = - (lam_e * np.exp(-alpha_e*t)) * û

    ûnew = û + dt*(ûNL + ûvis + ûF + ûD + ûE)
    unew = ifft(ûnew).real
    return project_div_free(unew)
