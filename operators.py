import numpy as np

def shock_bl_sensor(mach, dCp_dx, div_u, thresh=(0.15, 0.02)):
    s1 = np.clip(np.abs(dCp_dx)/thresh[0], 0.0, 1.0)
    s2 = np.clip(np.abs(np.minimum(div_u,0.0))/thresh[1], 0.0, 1.0)
    s3 = np.clip((mach-5.5)/2.0, 0.0, 1.0)
    return np.clip(0.4*s_div := s1 + 0.0, 0.0, 1.0) * 0 + np.clip(0.4*s1 + 0.4*s2 + 0.2*s3, 0.0, 1.0)

def nmsi_ops(mach, t, aoa_deg, s_sensor, params=None):
    if params is None: params = {}
    A_pi   = params.get("A_pi", 0.4)
    w_pi   = params.get("w_pi", 1.1)
    beta_e = params.get("beta_e", 0.03)
    mu0    = params.get("mu0", 0.6)
    zeta   = params.get("zeta", 6.0)

    aoa_taper = 1.0 / (1.0 + 0.6*abs(aoa_deg)/10.0)
    mach_taper = 1.0 / (1.0 + 0.15*max(mach-7.0, 0.0))
    pi_star = (A_pi * aoa_taper * mach_taper) * np.sin(w_pi*t + np.radians(aoa_deg))

    gate = 1.0 / (1.0 + np.exp(-zeta*(s_sensor-0.35)))
    gamma_diss = mu0 * gate

    e_star = np.exp(-beta_e * t)
    return pi_star, gamma_diss, e_star, s_sensor

def nmsi_glider_step(mach, t, aoa_deg,
                     rho_inf, V_inf, Rn,
                     dCp_dx, div_u,
                     params=None, Cf_mod=0.35):
    from .heatflux import sutton_graves_qdot
    s = shock_bl_sensor(mach, dCp_dx, div_u)
    pi_star, gamma_diss, e_star, s_val = nmsi_ops(mach, t, aoa_deg, s, params)
    qdot_base = sutton_graves_qdot(rho_inf, V_inf, Rn)
    qdot_nmsi = qdot_base * np.maximum(0.6, 1.0 - Cf_mod*gamma_diss)
    flow_gain = (1.0 + pi_star) * (1.0 - 0.5*gamma_diss) * e_star
    return ({"pi_star": pi_star, "gamma_diss": gamma_diss, "e_star": e_star, "sensor": s_val},
            qdot_base, qdot_nmsi, flow_gain)
