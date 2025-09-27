import numpy as np
from nmsi_sensors import gamma_diss_from_sensor

def nusgs_nmsi(nusgs, sensor, alpha_sgs=0.3):
    gamma = gamma_diss_from_sensor(sensor)
    return nusgs * (1.0 - alpha_sgs * gamma)
