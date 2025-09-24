
import numpy as np
import matplotlib.pyplot as plt

# Încărcăm datele demo
data = np.load('demo_timeseries.npz')

t = data['t']
energy_aug = data['energy_aug']
energy_cls = data['energy_cls']
enstrophy_aug = data['enstrophy_aug']
enstrophy_cls = data['enstrophy_cls']
vorticity_aug = data['vorticity_aug']
vorticity_cls = data['vorticity_cls']

plt.figure(figsize=(10,6))
plt.plot(t, energy_cls, label='Classical NSE Energy', linestyle='--')
plt.plot(t, energy_aug, label='Augmented NSE Energy')
plt.xlabel('Time')
plt.ylabel('Energy')
plt.legend()
plt.title('Energy comparison')
plt.show()

plt.figure(figsize=(10,6))
plt.plot(t, enstrophy_cls, label='Classical NSE Enstrophy', linestyle='--')
plt.plot(t, enstrophy_aug, label='Augmented NSE Enstrophy')
plt.xlabel('Time')
plt.ylabel('Enstrophy')
plt.legend()
plt.title('Enstrophy comparison')
plt.show()

plt.figure(figsize=(10,6))
plt.plot(t, vorticity_cls, label='Classical NSE Vorticity', linestyle='--')
plt.plot(t, vorticity_aug, label='Augmented NSE Vorticity')
plt.xlabel('Time')
plt.ylabel('Max Vorticity')
plt.legend()
plt.title('Vorticity comparison')
plt.show()
