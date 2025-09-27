import numpy as np
from nmsi_glider.core.operators import nmsi_glider_step

def komega_nmsi(mach, t, aoa_deg,
                rho_inf=0.015, V_inf=2100.0, Rn=0.05,
                dCp_dx=0.18, div_u=-0.03,
                params=None, Cf_mod=0.35,
                Cmu=0.09, kappa=0.41, clip_eps=1e-9):
    ops, q0, qN, gain = nmsi_glider_step(
        mach=mach, t=t, aoa_deg=aoa_deg,
        rho_inf=rho_inf, V_inf=V_inf, Rn=Rn,
        dCp_dx=dCp_dx, div_u=div_u,
        params=params, Cf_mod=Cf_mod
    )
    pi_star = ops["pi_star"]; gamma_d = ops["gamma_diss"]; e_star = ops["e_star"]
    k = (kappa*V_inf)**2 * np.clip(gamma_d, 0.0, 1.0)
    omega = k / (Cmu * (e_star + clip_eps))
    alpha = 0.10
    ratio = np.clip(k/(omega + clip_eps), 0.0, 0.8)
    q_turb = q0 * (1.0 - alpha * ratio)
    return {"q_base": q0, "q_nmsi": qN, "q_turb": q_turb,
            "reduction_pct": 100.0*(q0-q_turb)/max(q0, clip_eps),
            "k": k, "omega": omega, "ops": ops}
