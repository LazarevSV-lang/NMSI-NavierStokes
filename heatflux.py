import numpy as np

def sutton_graves_qdot(rho_inf, V_inf, Rn, k_SG=1.83e-4):
    rho = np.maximum(rho_inf, 1e-9)
    Rn  = np.maximum(Rn, 1e-6)
    return k_SG * np.sqrt(rho/Rn) * (V_inf**3)
