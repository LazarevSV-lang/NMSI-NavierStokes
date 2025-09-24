import numpy as np
from operators import e_term_physical, e_operator_factor, pi_star_factor

# Verify e-operator closed form
rng = np.random.default_rng(0)
u0 = rng.standard_normal((64,64))*0.1
u = u0.copy()
lam_e, alpha_e = 0.6, 0.25
dt, T = 1e-3, 3.0
t = 0.0
for _ in range(int(T/dt)):
    u = u + dt*e_term_physical(u, t, lam_e, alpha_e)
    t += dt

ref = u0 * np.exp(-(lam_e/alpha_e)*(1.0 - np.exp(-alpha_e*T)))
rel_err = np.linalg.norm(u - ref) / (np.linalg.norm(ref) + 1e-14)
print(f"e-operator check — relative L2 error: {rel_err:.3e}")

# π* zero mean check
A_pi, omega_pi = 0.15, 3.5
T = 2*np.pi/omega_pi
ts = np.linspace(0, T, 2001)
mean_over_period = np.trapz(A_pi*np.sin(omega_pi*ts), ts) / T
print(f"π* zero-mean over one period ~ {mean_over_period:.3e}")
