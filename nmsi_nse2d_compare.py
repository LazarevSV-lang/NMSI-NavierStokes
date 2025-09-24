import numpy as np
import matplotlib.pyplot as plt

# Simple 2D Navier-Stokes energy/enstrophy comparison (classical vs augmented NMSI)
def run_simulation(augmented=True, steps=2000, dt=1e-3):
    nx, ny = 64, 64
    u = np.zeros((nx, ny))
    v = np.zeros((nx, ny))
    energy = []
    enstrophy = []
    for t in range(steps):
        # toy update scheme (not physical)
        u += dt * (np.roll(v,1,axis=0) - np.roll(v,-1,axis=0))
        v += dt * (np.roll(u,1,axis=1) - np.roll(u,-1,axis=1))

        if augmented:
            # π* forcing: bounded oscillatory
            u += 0.01*np.sin(2*np.pi*t*dt)
            v += 0.01*np.cos(2*np.pi*t*dt)
            # γ_diss: damping
            u *= np.exp(-1e-3)
            v *= np.exp(-1e-3)

        e = np.mean(u**2 + v**2)
        w = np.mean((np.roll(v,-1,axis=0)-np.roll(v,1,axis=0) - (np.roll(u,-1,axis=1)-np.roll(u,1,axis=1)))**2)
        energy.append(e)
        enstrophy.append(w)
    return np.array(energy), np.array(enstrophy)

if __name__ == "__main__":
    e_classical, w_classical = run_simulation(augmented=False)
    e_aug, w_aug = run_simulation(augmented=True)

    np.savetxt("energy_classical.csv", e_classical, delimiter=",")
    np.savetxt("enstrophy_classical.csv", w_classical, delimiter=",")
    np.savetxt("energy_augmented.csv", e_aug, delimiter=",")
    np.savetxt("enstrophy_augmented.csv", w_aug, delimiter=",")

    plt.plot(e_classical, label="Classical NSE Energy")
    plt.plot(e_aug, label="Augmented NMSI Energy")
    plt.legend()
    plt.savefig("energy_comparison.png")
    plt.close()

    plt.plot(w_classical, label="Classical NSE Enstrophy")
    plt.plot(w_aug, label="Augmented NMSI Enstrophy")
    plt.legend()
    plt.savefig("enstrophy_comparison.png")
