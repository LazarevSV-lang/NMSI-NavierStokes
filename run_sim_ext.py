import numpy as np
import matplotlib.pyplot as plt
from src.mhd_twoflow_nmsi import twoflow_step
from src.cairo_stft import cairo_residual

u1, u2 = 1.0, 0.5
dt = 0.01
params = (0.1, 0.05, 0.01)
steps = 1000

series1, series2 = [], []
for _ in range(steps):
    u1, u2 = twoflow_step(u1,u2,dt,params)
    series1.append(u1)
    series2.append(u2)

np.savetxt('outputs/timeseries.csv', np.c_[series1,series2], delimiter=',')
plt.plot(series1, label='u1')
plt.plot(series2, label='u2')
plt.legend()
plt.savefig('outputs/fig_states.png')
