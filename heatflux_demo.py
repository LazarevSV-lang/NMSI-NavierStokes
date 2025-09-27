import numpy as np
import matplotlib.pyplot as plt
from nmsi_sensors import gamma_diss_from_sensor

def qdot_base(mach, rho=0.015, V=2100, Rn=0.05):
    return 0.763 * rho**0.5 * V**3 / np.sqrt(Rn)

def qdot_nmsi(mach, t, aoa, rho=0.015, V=2100, Rn=0.05):
    q0 = qdot_base(mach, rho, V, Rn)
    gamma = np.exp(-mach/8) * (1 - aoa/10)
    e = np.exp(-t*0.03)
    return q0 * gamma * e

if __name__ == "__main__":
    times = np.linspace(0, 20, 100)
    q_bases = [qdot_base(7) for t in times]
    q_nmsis = [qdot_nmsi(7, t, 5) for t in times]

    plt.plot(times, q_bases, label="Base NS")
    plt.plot(times, q_nmsis, label="NMSI-augmented")
    plt.xlabel("t")
    plt.ylabel("q_dot [W/cm^2] (scaled)")
    plt.legend()
    plt.grid(True)
    plt.savefig("heatflux_demo.png")
    print("Saved plot heatflux_demo.png")
