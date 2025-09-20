#!/usr/bin/env python3
"""
2D augmented NSE demo (finite‑difference) — fast run for energy/enstrophy control.
"""
import argparse, numpy as np, os, yaml, csv

def parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, default="config.yaml")
    return ap.parse_args()

def curl_z(u, v, dx, dy):
    dvdx = (np.roll(v, -1, axis=1) - np.roll(v, 1, axis=1))/(2*dx)
    dudy = (np.roll(u, -1, axis=0) - np.roll(u, 1, axis=0))/(2*dy)
    return dvdx - dudy

def laplacian(f, dx, dy):
    return ((np.roll(f,-1,axis=0)-2*f+np.roll(f,1,axis=0))/dy**2 +
            (np.roll(f,-1,axis=1)-2*f+np.roll(f,1,axis=1))/dx**2)

def advect(u, v, f, dx, dy):
    dudx = (np.roll(f, -1, axis=1) - np.roll(f, 1, axis=1))/(2*dx)
    dudy = (np.roll(f, -1, axis=0) - np.roll(f, 1, axis=0))/(2*dy)
    return u*dudx + v*dudy

def proj_incompressible(u, v, dx, dy, iters=40):
    div = (np.roll(u, -1, axis=1) - np.roll(u, 1, axis=1))/(2*dx) + \
          (np.roll(v, -1, axis=0) - np.roll(v, 1, axis=0))/(2*dy)
    p = np.zeros_like(u)
    for _ in range(iters):
        p = 0.25*(np.roll(p,-1,axis=1)+np.roll(p,1,axis=1)+np.roll(p,-1,axis=0)+np.roll(p,1,axis=0) - div*dx*dy)
    u -= (np.roll(p, -1, axis=1) - np.roll(p, 1, axis=1))/(2*dx)
    v -= (np.roll(p, -1, axis=0) - np.roll(p, 1, axis=0))/(2*dy)
    return u, v

def main():
    args = parse()
    cfg = yaml.safe_load(open(args.config))

    nx = cfg["grid"]["nx"]; ny = cfg["grid"]["ny"]
    Lx = cfg["grid"]["Lx"]; Ly = cfg["grid"]["Ly"]
    nu = cfg["physics"]["nu"]
    A_pi = cfg["forcing_pi"]["A_pi"]; omega_pi = cfg["forcing_pi"]["omega_pi"]; phi = cfg["forcing_pi"]["phi"]
    gamma0 = cfg["gamma_diss"]["gamma0"]; omegaZ = cfg["gamma_diss"]["omega_Z"]; phiZ = cfg["gamma_diss"]["phiZ"]; zeta = cfg["gamma_diss"]["zeta"]

    dx = Lx/nx; dy = Ly/ny
    x = np.linspace(0, Lx, nx, endpoint=False)
    y = np.linspace(0, Ly, ny, endpoint=False)
    X, Y = np.meshgrid(x, y)

    U0 = 1.0
    u =  U0*np.sin(X)*np.cos(Y)
    v = -U0*np.cos(X)*np.sin(Y)

    t = 0.0; t_end = cfg["time"]["t_end"]
    dt = min(cfg["time"]["dt_max"], 0.2*min(dx,dy)/max(U0,1e-6))
    save_every = cfg["time"]["save_every"]

    out_csv = os.path.join(".", "out_2d_diag.csv")
    with open(out_csv, "w", newline="") as f:
        csv.writer(f).writerow(["t","E","Omega","Wmax"])

    istep = 0
    while t < t_end:
        Fux = A_pi*np.cos(omega_pi*t + phi)*u
        Fvy = A_pi*np.cos(omega_pi*t + phi)*v

        gate = 1.0 if np.sin(omegaZ*t + phiZ) > zeta else 0.0
        gamma_t = gamma0*gate

        u_star = u + dt*(-advect(u,v,u,dx,dy) + nu*laplacian(u,dx,dy) + Fux - gamma_t*u)
        v_star = v + dt*(-advect(u,v,v,dx,dy) + nu*laplacian(v,dx,dy) + Fvy - gamma_t*v)

        u, v = proj_incompressible(u_star, v_star, dx, dy, iters=40)

        omega = curl_z(u, v, dx, dy)
        E = 0.5*np.mean(u*u + v*v)
        Omega = 0.5*np.mean(omega*omega)
        Wmax = np.abs(omega).max()

        if istep % max(1, save_every) == 0:
            with open(out_csv, "a", newline="") as f:
                csv.writer(f).writerow([t, E, Omega, Wmax])

        t += dt; istep += 1

    print(f"Done. Diagnostics saved to {out_csv}")

if __name__ == "__main__":
    main()
