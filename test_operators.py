import numpy as np
from core.operators import nmsi_glider_step

def test_basic_step():
    ops, q0, qN, gain = nmsi_glider_step(
        mach=7.0, t=10.0, aoa_deg=5.0,
        rho_inf=0.015, V_inf=2100.0, Rn=0.05,
        dCp_dx=0.2, div_u=-0.03,
        params={"A_pi":0.35,"w_pi":1.2,"beta_e":0.03,"mu0":0.55,"zeta":6.0},
        Cf_mod=0.35
    )
    assert qN <= q0
    assert 0.0 <= ops['sensor'] <= 1.0
