import numpy as np

def ducros_sensor(divU, vort_mag, dCp_dx, M, Cp_th=0.15, lam=(0.5,0.3,0.2)):
    s_div = (np.minimum(divU,0.0)**2)/(np.minimum(divU,0.0)**2 + vort_mag**2 + 1e-12)
    s_cp  = np.clip(np.abs(dCp_dx)/Cp_th, 0.0, 1.0)
    s_m   = np.clip((M-5.5)/2.0, 0.0, 1.0)
    l1,l2,l3 = lam
    return np.clip(l1*s_div + l2*s_cp + l3*s_m, 0.0, 1.0)

def gamma_diss_from_sensor(s, mu0=0.6, zeta=6.0, s0=0.35):
    return mu0/(1.0 + np.exp(-zeta*(s - s0)))
