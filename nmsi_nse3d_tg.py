#!/usr/bin/env python3
"""
NMSI–π*–HDQG augmented incompressible NSE (3D) — Taylor–Green vortex (pseudo‑spectral skeleton).

Notes:
- Educational code (NumPy FFT); use MPI/CUDA for research‑grade runs.
- Helmholtz projection enforces incompressibility in spectral space.
- π* forcing is band‑limited and bounded; γ_diss acts intermittently (Z‑windows).
"""
import argparse, os
import numpy as np
import yaml

def parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, default="config.yaml")
    return ap.parse_args()

def helmholtz_project(kx, ky, kz, U):
    k2 = kx**2 + ky**2 + kz**2
    with np.errstate(divide='ignore', invalid='ignore'):
        dot = (kx*U[0] + ky*U[1] + kz*U[2])
        proj = U - np.stack([kx*dot, ky*dot, kz*dot], axis=0) / np.where(k2==0, 1, k2)
    proj[:, k2==0] = 0.0
    return proj

def rectangular_dealias(nx, ny, nz, use=True):
    if not use:
        return np.ones((nx,ny,nz), float)
    mx, my, mz = nx//3, ny//3, nz//3
    M = np.zeros((nx,ny,nz), float)
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                okx = (i <= mx) or (i >= nx-mx)
                oky = (j <= my) or (j >= ny-my)
                okz = (k <= mz) or (k >= nz-mz)
                M[i,j,k] = 1.0 if (okx and oky and okz) else 0.0
    return M

def shell_band(kmag, k1, k2):
    return np.logical_and(kmag>=k1, kmag<=k2).astype(float)

def main():
    args = parse()
    cfg = yaml.safe_load(open(args.config))

    nx, ny, nz = cfg["grid"]["nx"], cfg["grid"]["ny"], cfg["grid"]["nz"]
    Lx, Ly, Lz = cfg["grid"]["Lx"], cfg["grid"]["Ly"], cfg["grid"]["Lz"]
    nu = cfg["physics"]["nu"]
    A_pi = cfg["forcing_pi"]["A_pi"]; omega_pi = cfg["forcing_pi"]["omega_pi"]; phi = cfg["forcing_pi"]["phi"]
    k1 = cfg["forcing_pi"]["k1"]; k2 = cfg["forcing_pi"]["k2"]; use_pi = cfg["forcing_pi"]["use"]
    use_band = cfg["forcing_pi"]["bandpass"]
    gamma0 = cfg["gamma_diss"]["gamma0"]; omegaZ = cfg["gamma_diss"]["omega_Z"]
    phiZ = cfg["gamma_diss"]["phiZ"]; zeta = cfg["gamma_diss"]["zeta"]; use_gamma = cfg["gamma_diss"]["use"]
    dealias_use = cfg["dealias"]["use"]
    outdir = cfg["io"]["outdir"]; os.makedirs(outdir, exist_ok=True)

    # Spectral grid
    kx = 2*np.pi*np.fft.fftfreq(nx, d=Lx/nx)
    ky = 2*np.pi*np.fft.fftfreq(ny, d=Ly/ny)
    kz = 2*np.pi*np.fft.fftfreq(nz, d=Lz/nz)
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
    K2 = KX**2 + KY**2 + KZ**2
    Kmag = np.sqrt(K2)
    mask = rectangular_dealias(nx, ny, nz, use=dealias_use)

    # Initial condition: Taylor–Green
    x = np.linspace(0, Lx, nx, endpoint=False)
    y = np.linspace(0, Ly, ny, endpoint=False)
    z = np.linspace(0, Lz, nz, endpoint=False)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    U0 = 1.0
    u0 = np.zeros((3, nx, ny, nz), float)
    u0[0] =  U0*np.sin(X)*np.cos(Y)*np.cos(Z)
    u0[1] = -U0*np.cos(X)*np.sin(Y)*np.cos(Z)
    u0[2] =  0.0

    uhat = np.fft.fftn(u0, axes=(1,2,3))
    uhat = helmholtz_project(KX, KY, KZ, uhat)

    # Time params
    t, t_end = 0.0, cfg["time"]["t_end"]
    cfl, dt_min, dt_max = cfg["time"]["cfl"], cfg["time"]["dt_min"], cfg["time"]["dt_max"]
    save_every = cfg["time"]["save_every"]; istep = 0

    # Diagnostics
    times, E_list, Omega_list, Wmax_list = [], [], [], []

    def to_phys(Uhat): return np.fft.ifftn(Uhat, axes=(1,2,3)).real

    while t < t_end:
        u = to_phys(uhat)
        umax = max(np.abs(u[0]).max(), np.abs(u[1]).max(), np.abs(u[2]).max())
        dx = min(Lx/nx, Ly/ny, Lz/nz)
        dt = min(dt_max, max(dt_min, cfl * dx / (umax + 1e-8)))

        # Nonlinear convective term
        ux = np.fft.fftn(u[0], axes=(0,1,2)); uy = np.fft.fftn(u[1], axes=(0,1,2)); uz = np.fft.fftn(u[2], axes=(0,1,2))
        ikx, iky, ikz = 1j*KX, 1j*KY, 1j*KZ
        dux_dx = np.fft.ifftn(ikx*ux, axes=(0,1,2)).real
        dux_dy = np.fft.ifftn(iky*ux, axes=(0,1,2)).real
        dux_dz = np.fft.ifftn(ikz*ux, axes=(0,1,2)).real
        duy_dx = np.fft.ifftn(ikx*uy, axes=(0,1,2)).real
        duy_dy = np.fft.ifftn(iky*uy, axes=(0,1,2)).real
        duy_dz = np.fft.ifftn(ikz*uy, axes=(0,1,2)).real
        duz_dx = np.fft.ifftn(ikx*uz, axes=(0,1,2)).real
        duz_dy = np.fft.ifftn(iky*uz, axes=(0,1,2)).real
        duz_dz = np.fft.ifftn(ikz*uz, axes=(0,1,2)).real
        conv = np.stack([
            u[0]*dux_dx + u[1]*dux_dy + u[2]*dux_dz,
            u[0]*duy_dx + u[1]*duy_dy + u[2]*duy_dz,
            u[0]*duz_dx + u[1]*duz_dy + u[2]*duz_dz
        ], axis=0)
        conv_hat = np.fft.fftn(conv, axes=(1,2,3))

        # Viscosity
        visc_hat = -nu * K2 * uhat

        # π* forcing
        if use_pi:
            shell = shell_band(Kmag, k1, k2) if use_band else np.ones_like(Kmag)
            Fhat = A_pi * np.cos(omega_pi*t + phi) * shell * uhat
        else:
            Fhat = 0.0

        # Intermittent γ_diss
        if use_gamma:
            gate = 1.0 if np.sin(omegaZ*t + phiZ) > zeta else 0.0
            gamma_t = gamma0 * gate
        else:
            gamma_t = 0.0
        gamma_hat = -gamma_t * uhat

        # RHS and projection
        rhs = -(conv_hat) + visc_hat + Fhat + gamma_hat
        rhs = helmholtz_project(KX, KY, KZ, rhs)
        rhs *= mask

        # Step (Euler for simplicity)
        uhat = uhat + dt * rhs
        uhat *= mask

        # Diagnostics
        u = to_phys(uhat)
        wx = (np.fft.ifftn(1j*KZ*uhat[1] - 1j*KY*uhat[2], axes=(1,2,3))).real
        wy = (np.fft.ifftn(1j*KX*uhat[2] - 1j*KZ*uhat[0], axes=(1,2,3))).real
        wz = (np.fft.ifftn(1j*KY*uhat[0] - 1j*KX*uhat[1], axes=(1,2,3))).real
        w2 = wx**2 + wy**2 + wz**2
        E = 0.5*np.mean(u[0]**2 + u[1]**2 + u[2]**2)
        Omega = 0.5*np.mean(w2)
        Wmax = np.sqrt(w2.max())
        times.append(t); E_list.append(E); Omega_list.append(Omega); Wmax_list.append(Wmax)

        t += dt; istep += 1
        if istep % max(1, save_every) == 0:
            np.savez(os.path.join(outdir, f"diag_{istep:06d}.npz"),
                     t=np.array(times), E=np.array(E_list),
                     Omega=np.array(Omega_list), Wmax=np.array(Wmax_list))

    np.savez(os.path.join(outdir, "final_timeseries.npz"),
             t=np.array(times), E=np.array(E_list),
             Omega=np.array(Omega_list), Wmax=np.array(Wmax_list))

if __name__ == "__main__":
    main()
