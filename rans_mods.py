import numpy as np
from nmsi_sensors import gamma_diss_from_sensor

def nut_nmsi(nut, sensor, alpha_nut=0.5):
    gamma = gamma_diss_from_sensor(sensor)
    return nut * (1.0 - alpha_nut * gamma)

def Pk_nmsi(Pk, sensor, alpha_P=0.25):
    gamma = gamma_diss_from_sensor(sensor)
    return Pk * (1.0 - alpha_P * gamma)
