#!/usr/bin/env python3
# Upgraded 3D NSE (NMSI–π*–HDQG): SSPRK3 + spherical dealias + energy budget + compare_mode
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

def spherical_dealias(KX, KY, KZ, frac=2/3):
    Kmag = np.sqrt(KX**2 + KY**2 + KZ**2)
    kx_max = np.max(np.abs(KX)); ky_max = np.max(np.abs(KY)); kz_max = np.max(np.abs(KZ))
    kmax = min(kx_max, ky_max, kz_max); cutoff = frac * kmax
    return (Kmag <= cutoff).astype(float), Kmag

def shell_band(Kmag, k1, k2):
    return np.logical_and(Kmag>=k1, Kmag<=k2).astype(float)

def main():
    args = parse(); cfg = yaml.safe_load(open(args.config))
    nx, ny, nz = cfg["grid"]["nx"], cfg["grid"]["ny"], cfg["grid"]["nz"]
    Lx, Ly, Lz = cfg["grid"]["Lx"], cfg["grid"]["Ly"], cfg["grid"]["Lz"]
    nu = cfg["physics"]["nu"]; use_dealias = cfg.get("dealias",{}).get("use", True)

    fcfg = cfg["forcing_pi"]; gcfg = cfg["gamma_diss"]
    A_pi, omega_pi, phi = fcfg["A_pi"], fcfg["omega_pi"], fcfg["phi"]
    k1, k2 = fcfg["k1"], fcfg["k2"]; use_pi = fcfg.get("use", True); use_band = fcfg.get("bandpass", True)
    gamma0, omegaZ, phiZ, zeta = gcfg["gamma0"], gcfg["omega_Z"], gcfg["phiZ"], gcfg["zeta"]
    use_gamma = gcfg.get("use", True)

    use_classical = cfg.get("compare_mode",{}).get("classical", False)
    if use_classical: use_pi=False; use_gamma=False

    kx = 2*np.pi*np.fft.fftfreq(nx, d=Lx/nx)
    ky = 2*np.pi*np.fft.fftfreq(ny, d=Ly/ny)
    kz = 2*np.pi*np.fft.fftfreq(nz, d=Lz/nz)
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
    K2 = KX**2 + KY**2 + KZ**2
    mask, Kmag = spherical_dealias(KX, KY, KZ, 2/3) if use_dealias else (np.ones((nx,ny,nz)), np.sqrt(K2))

    x = np.linspace(0, Lx, nx, endpoint=False)
    y = np.linspace(0, Ly, ny, endpoint=False)
    z = np.linspace(0, Lz, nz, endpoint=False)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    U0 = 1.0
    u0 = np.zeros((3, nx, ny, nz), float)
    u0[0] =  U0*np.sin(X)*np.cos(Y)*np.cos(Z)
    u0[1] = -U0*np.cos(X)*np.sin(Y)*np.cos(Z)
    u0[2] =  0.0
    uhat = np.fft.fftn(u0, axes=(1,2,3)); uhat = helmholtz_project(KX, KY, KZ, uhat)

    t = 0.0; t_end = cfg["time"]["t_end"]; cfl = cfg["time"]["cfl"]
    dt_min = cfg["time"]["dt_min"]; dt_max = cfg["time"]["dt_max"]; save_every = cfg["time"]["save_every"]; istep=0
    outdir = cfg.get("io",{}).get("outdir","./out_3d"); os.makedirs(outdir, exist_ok=True)

    times=[]; E_list=[]; Omega_list=[]; Wmax_list=[]; InjPi_list=[]; EpsNu_list=[]; EpsGamma_list=[]

    def phys(uh): return np.fft.ifftn(uh, axes=(1,2,3)).real
    def grad(ucomp):
        return (np.fft.ifftn(1j*KX*np.fft.fftn(ucomp, axes=(0,1,2)), axes=(0,1,2)).real,
                np.fft.ifftn(1j*KY*np.fft.fftn(ucomp, axes=(0,1,2)), axes=(0,1,2)).real,
                np.fft.ifftn(1j*KZ*np.fft.fftn(ucomp, axes=(0,1,2)), axes=(0,1,2)).real)
    def RHS(uh, tloc):
        u = phys(uh)
        dux_dx, dux_dy, dux_dz = grad(u[0])
        duy_dx, duy_dy, duy_dz = grad(u[1])
        duz_dx, duz_dy, duz_dz = grad(u[2])
        conv = np.stack([
            u[0]*dux_dx + u[1]*dux_dy + u[2]*dux_dz,
            u[0]*duy_dx + u[1]*duy_dy + u[2]*duz_dz,
            u[0]*duz_dx + u[1]*duz_dy + u[2]*duz_dz
        ], axis=0)
        conv_hat = np.fft.fftn(conv, axes=(1,2,3))
        visc_hat = -nu * K2 * uh
        if use_pi:
            shell = shell_band(Kmag, k1, k2) if use_band else np.ones_like(Kmag)
            Fhat = A_pi*np.cos(omega_pi*tloc + phi)*shell*uh
        else:
            Fhat = 0.0
        if use_gamma:
            gate = 1.0 if np.sin(omegaZ*tloc + phiZ) > zeta else 0.0
            gamma_t = gamma0*gate
        else:
            gamma_t = 0.0
        gamma_hat = -gamma_t * uh
        rhs = -(conv_hat) + visc_hat + Fhat + gamma_hat
        rhs = helmholtz_project(KX, KY, KZ, rhs); rhs *= mask
        return rhs, gamma_t

    while t < t_end:
        u = phys(uhat)
        umax = max(np.abs(u[0]).max(), np.abs(u[1]).max(), np.abs(u[2]).max())
        dx_min = min(Lx/nx, Ly/ny, Lz/nz)
        dt = min(dt_max, max(dt_min, cfl * dx_min / (umax + 1e-8)))

        rhs1, g1 = RHS(uhat, t);      uh1 = uhat + dt*rhs1
        rhs2, g2 = RHS(uh1, t+dt);    uh2 = 0.75*uhat + 0.25*(uh1 + dt*rhs2)
        rhs3, g3 = RHS(uh2, t+0.5*dt); uhat = (1/3)*uhat + (2/3)*(uh2 + dt*rhs3)
        uhat *= mask

        u = phys(uhat)
        wx = (np.fft.ifftn(1j*KZ*uhat[1] - 1j*KY*uhat[2], axes=(1,2,3))).real
        wy = (np.fft.ifftn(1j*KX*uhat[2] - 1j*KZ*uhat[0], axes=(1,2,3))).real
        wz = (np.fft.ifftn(1j*KY*uhat[0] - 1j*KX*uhat[1], axes=(1,2,3))).real
        w2 = wx**2 + wy**2 + wz**2
        E = 0.5*np.mean(u[0]**2 + u[1]**2 + u[2]**2)
        Omega = 0.5*np.mean(w2)
        Wmax = np.sqrt(w2.max())

        gx = grad(u[0]); gy = grad(u[1]); gz = grad(u[2])
        grad_u_sq = sum(g**2 for g in gx) + sum(g**2 for g in gy) + sum(g**2 for g in gz)
        eps_nu = nu * np.mean(grad_u_sq)
        eps_gamma = ((g1+g2+g3)/3.0) * np.mean(u[0]**2 + u[1]**2 + u[2]**2) if use_gamma else 0.0
        inj_pi = (A_pi*np.cos(omega_pi*t + phi) * np.mean(u[0]**2 + u[1]**2 + u[2]**2)) if use_pi else 0.0

        times.append(t); E_list.append(E); Omega_list.append(Omega); Wmax_list.append(Wmax)
        EpsNu_list.append(eps_nu); EpsGamma_list.append(eps_gamma); InjPi_list.append(inj_pi)

        t += dt; istep += 1
        if istep % max(1, save_every) == 0:
            np.savez(os.path.join(outdir, f"diag_{istep:06d}.npz"),
                     t=np.array(times), E=np.array(E_list),
                     Omega=np.array(Omega_list), Wmax=np.array(Wmax_list),
                     eps_nu=np.array(EpsNu_list), eps_gamma=np.array(EpsGamma_list),
                     inj_pi=np.array(InjPi_list))

    np.savez(os.path.join(outdir, "final_timeseries.npz"),
             t=np.array(times), E=np.array(E_list),
             Omega=np.array(Omega_list), Wmax=np.array(Wmax_list),
             eps_nu=np.array(EpsNu_list), eps_gamma=np.array(EpsGamma_list),
             inj_pi=np.array(InjPi_list))

if __name__ == "__main__":
    main()
