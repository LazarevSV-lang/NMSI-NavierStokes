import numpy as np
from e_operator import e_term_physical

# Verification test of the e-operator
rng = np.random.default_rng(0)
u0 = rng.standard_normal((64, 64)) * 0.1  # synthetic field
u_num = u0.copy()

lam_e, alpha_e = 0.6, 0.25
T, dt = 3.0, 1e-3
steps = int(T/dt)

t = 0.0
for _ in range(steps):
    u_num = u_num + dt * e_term_physical(u_num, t, lam_e, alpha_e)
    t += dt

# closed-form reference
ref_factor = np.exp(-(lam_e/alpha_e) * (1.0 - np.exp(-alpha_e * T)))
u_ref = u0 * ref_factor

# errors
rel_err = np.linalg.norm(u_num - u_ref) / (np.linalg.norm(u_ref) + 1e-14)
print(f"Closed-form factor at T={T}: {ref_factor:.6f}")
print(f"Relative L2 error (num vs exact): {rel_err:.3e}")
