import numpy as np
from e_operator import e_term_physical

def energy(u, v):
    return 0.5*np.mean(u*u + v*v)

def enstrophy(u, v):
    vx = np.roll(v, -1, axis=1) - np.roll(v, 1, axis=1)
    uy = np.roll(u, -1, axis=0) - np.roll(u, 1, axis=0)
    w  = vx - uy
    return np.mean(w*w)

nx, ny = 64, 64
rng = np.random.default_rng(0)
u = rng.standard_normal((nx, ny)) * 0.1
v = rng.standard_normal((nx, ny)) * 0.1

lam_e, alpha_e = 0.6, 0.25
dt, T = 1e-2, 3.0
steps = int(T/dt)

E_hist, Z_hist, T_hist = [], [], []
t = 0.0
for k in range(steps):
    eu, ev = e_term_physical([u, v], t, lam_e=lam_e, alpha_e=alpha_e)
    u = u + dt*eu
    v = v + dt*ev
    t += dt
    if k % 10 == 0:
        E_hist.append(energy(u, v))
        Z_hist.append(enstrophy(u, v))
        T_hist.append(t)

print(f"E(0) -> E(T): {E_hist[0]:.6f} -> {E_hist[-1]:.6f}")
print(f"max Ω(t): {np.max(Z_hist):.6f}")
