
import argparse, os
import numpy as np
import matplotlib.pyplot as plt

def make_grid(nx, ny, Lx=2*np.pi, Ly=2*np.pi):
    dx, dy = Lx/nx, Ly/ny
    x = np.arange(nx)*dx; y = np.arange(ny)*dy
    X, Y = np.meshgrid(x, y, indexing='ij')
    kx = np.fft.fftfreq(nx, d=dx/(2*np.pi))
    ky = np.fft.fftfreq(ny, d=dy/(2*np.pi))
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    return X, Y, KX, KY

def project_div_free(u, KX, KY, nx, ny):
    uhx = np.fft.rfftn(u[...,0], axes=(0,1))
    uhy = np.fft.rfftn(u[...,1], axes=(0,1))
    kxr = KX[:, :uhx.shape[1]]; kyr = KY[:, :uhx.shape[1]]
    K2r = (kxr**2 + kyr**2); K2r[0,0] = 1.0
    div_hat = kxr*uhx + kyr*uhy
    uhx -= kxr*div_hat/K2r; uhy -= kyr*div_hat/K2r
    ux = np.fft.irfftn(uhx, s=(nx,ny), axes=(0,1))
    uy = np.fft.irfftn(uhy, s=(nx,ny), axes=(0,1))
    return np.stack([ux, uy], axis=-1)

def grad(u, KX, KY, nx, ny):
    uhx = np.fft.rfftn(u[...,0], axes=(0,1))
    uhy = np.fft.rfftn(u[...,1], axes=(0,1))
    kxr = KX[:, :uhx.shape[1]]; kyr = KY[:, :uhx.shape[1]]
    ux_x = np.fft.irfftn(1j*kxr*uhx, s=(nx,ny), axes=(0,1))
    ux_y = np.fft.irfftn(1j*kyr*uhx, s=(nx,ny), axes=(0,1))


    uy_x = np.fft.irfftn(1j*kxr*uhy, s=(nx,ny), axes=(0,1))
    uy_y = np.fft.irfftn(1j*kyr*uhy, s=(nx,ny), axes=(0,1))
    return ux_x, ux_y, uy_x, uy_y

def nonlinear_term(u, KX, KY, nx, ny):
    ux_x, ux_y, uy_x, uy_y = grad(u, KX, KY, nx, ny)
    advx = u[...,0]*ux_x + u[...,1]*ux_y
    advy = u[...,0]*uy_x + u[...,1]*uy_y
    return -np.stack([advx, advy], axis=-1)

def laplacian(u, KX, KY, nx, ny):
    uhx = np.fft.rfftn(u[...,0], axes=(0,1))
    uhy = np.fft.rfftn(u[...,1], axes=(0,1))
    k2r = (KX[:, :uhx.shape[1]]**2 + KY[:, :uhx.shape[1]]**2)
    lx = np.fft.irfftn(-k2r*uhx, s=(nx,ny), axes=(0,1))
    ly = np.fft.irfftn(-k2r*uhy, s=(nx,ny), axes=(0,1))
    return np.stack([lx, ly], axis=-1)

def vorticity(u, KX, KY, nx, ny):
    ux_x, ux_y, uy_x, uy_y = grad(u, KX, KY, nx, ny)
    return uy_x - ux_y

def energy(u):
    return 0.5*np.mean((u**2).sum(-1))

def enstrophy(u, KX, KY, nx, ny):
    return np.mean(vorticity(u, KX, KY, nx, ny)**2)

def wmax(u, KX, KY, nx, ny):
    return np.abs(vorticity(u, KX, KY, nx, ny)).max()

def Z_window_k(KX, KY, uh):
    kxr = KX[:, :uh.shape[1]]; kyr = KY[:, :uh.shape[1]]
    kmag = np.sqrt(kxr**2 + kyr**2)
    kmax = kmag.max()
    Z = (kmag >= 0.6*kmax) & (kmag <= 0.9*kmax)
    return Z.astype(float)

def step(u, t, dt, nu, aug, params, KX, KY, nx, ny):
    NL  = nonlinear_term(u, KX, KY, nx, ny)
    visc= nu*laplacian(u, KX, KY, nx, ny)

    if aug:
        A_pi, omega_pi, phi = params["pi_amp"], params["pi_omega"], params.get("pi_phi",0.0)
        lam_e, alpha_e      = params["e_lambda"], params["e_alpha"]
        gamma0              = params["gamma0"]
        Fpi = A_pi*np.sin(omega_pi*t + phi)*u
    else:
        Fpi = 0.0*u

    uhx = np.fft.rfftn(u[...,0], axes=(0,1))
    uhy = np.fft.rfftn(u[...,1], axes=(0,1))
    if aug:
        Z = Z_window_k(KX, KY, uhx)
        uhx_new = uhx + dt*( np.fft.rfftn(NL[...,0]+visc[...,0]+Fpi[...,0], axes=(0,1))
                           - (gamma0*Z)*uhx - lam_e*np.exp(-alpha_e*t)*uhx )
        uhy_new = uhy + dt*( np.fft.rfftn(NL[...,1]+visc[...,1]+Fpi[...,1], axes=(0,1))
                           - (gamma0*Z)*uhy - lam_e*np.exp(-alpha_e*t)*uhy )
    else:
        uhx_new = uhx + dt*( np.fft.rfftn(NL[...,0]+visc[...,0], axes=(0,1)) )
        uhy_new = uhy + dt*( np.fft.rfftn(NL[...,1]+visc[...,1], axes=(0,1)) )

    ux = np.fft.irfftn(uhx_new, s=(nx,ny), axes=(0,1))
    uy = np.fft.irfftn(uhy_new, s=(nx,ny), axes=(0,1))
    unew = np.stack([ux, uy], axis=-1)
    return project_div_free(unew, KX, KY, nx, ny)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nx", type=int, default=64)
    ap.add_argument("--ny", type=int, default=64)
    ap.add_argument("--nu", type=float, default=1e-3)
    ap.add_argument("--t_end", type=float, default=4.0)
    ap.add_argument("--dt", type=float, default=2.5e-3)
    ap.add_argument("--aug", type=str, default="on", choices=["on","off"])
    ap.add_argument("--pi_amp", type=float, default=0.2)
    ap.add_argument("--pi_omega", type=float, default=2.0)
    ap.add_argument("--pi_phi", type=float, default=0.0)
    ap.add_argument("--e_lambda", type=float, default=0.4)
    ap.add_argument("--e_alpha", type=float, default=0.2)
    ap.add_argument("--gamma0", type=float, default=0.6)
    ap.add_argument("--outdir", type=str, default="out")
    args = ap.parse_args()

    nx, ny, nu, t_end, dt = args.nx, args.ny, args.nu, args.t_end, args.dt
    aug = (args.aug == "on")
    params = dict(pi_amp=args.pi_amp, pi_omega=args.pi_omega, pi_phi=args.pi_phi,
                  e_lambda=args.e_lambda, e_alpha=args.e_alpha, gamma0=args.gamma0)

    os.makedirs(args.outdir, exist_ok=True)

    X, Y, KX, KY = make_grid(nx, ny)
    u = np.zeros((nx,ny,2))
    u[...,0] =  np.sin(X)*np.cos(Y)
    u[...,1] = -np.cos(X)*np.sin(Y)
    u = project_div_free(u, KX, KY, nx, ny)

    times = []
    E_hist, Om_hist, W_hist = [], [], []
    t=0.0; nsteps = int(t_end/dt)
    for n in range(nsteps):
        u = step(u, t, dt, nu, aug, params, KX, KY, nx, ny)
        t += dt
        if n % 20 == 0:
            times.append(t)
            E_hist.append(0.5*np.mean((u**2).sum(-1)))
            Om_hist.append(enstrophy(u, KX, KY, nx, ny))
            W_hist.append(wmax(u, KX, KY, nx, ny))

    times = np.array(times); E_hist=np.array(E_hist); Om_hist=np.array(Om_hist); W_hist=np.array(W_hist)

    tag = "aug" if aug else "classical"
    np.savez(os.path.join(args.outdir, f"tg_{tag}_timeseries.npz"),
             t=times, E=E_hist, Om=Om_hist, W=W_hist,
             params=params, nx=nx, ny=ny, nu=nu, dt=dt)

    print(f"Saved: {os.path.join(args.outdir, f'tg_{tag}_timeseries.npz')}")
    print(f"Final: E={E_hist[-1]:.3e}, Ω={Om_hist[-1]:.3e}, max|ω|={W_hist[-1]:.3e}")

if __name__ == '__main__':
    main()
