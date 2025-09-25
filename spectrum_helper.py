import numpy as np
import matplotlib.pyplot as plt

def energy_spectrum(u, KX, KY):
    uhx = np.fft.rfftn(u[...,0], axes=(0,1))
    uhy = np.fft.rfftn(u[...,1], axes=(0,1))
    E = 0.5*(np.abs(uhx)**2 + np.abs(uhy)**2)
    kx = KX[:, :uhx.shape[1]]
    ky = KY[:, :uhx.shape[1]]
    kmag = np.sqrt(kx**2 + ky**2)
    kmax = int(kmag.max())
    Ek = np.zeros(kmax+1)
    for i in range(kmag.shape[0]):
        for j in range(kmag.shape[1]):
            kbin = int(round(kmag[i,j]))
            Ek[kbin] += E[i,j]
    return Ek

def plot_spectrum(Ek):
    k = np.arange(len(Ek))
    plt.loglog(k[1:], Ek[1:], '-o')
    plt.xlabel('k')
    plt.ylabel('E(k)')
    plt.title('Energy Spectrum')
    plt.tight_layout()
    plt.show()
