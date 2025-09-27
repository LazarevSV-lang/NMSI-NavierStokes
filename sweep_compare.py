import numpy as np
import csv
from nmsi_glider.core.operators import nmsi_glider_step

def run_case(A_pi, mu0, beta_e, t=10.0, mach=7.0, aoa=5.0,
             rho=0.015, V=2100.0, Rn=0.05, dcp=0.2, divu=-0.03, Cf_mod=0.35):
    params = {"A_pi":A_pi, "w_pi":1.2, "beta_e":beta_e, "mu0":mu0, "zeta":6.0}
    ops, q0, qN, gain = nmsi_glider_step(mach, t, aoa, rho, V, Rn, dcp, divu, params, Cf_mod)
    saving_pct = (q0-qN)/max(q0,1e-12)*100.0
    return q0, qN, saving_pct

if __name__ == "__main__":
    A_pis = [0.2, 0.3, 0.4]
    mu0s  = [0.4, 0.55, 0.7]
    betas = [0.02, 0.03, 0.05]
    rows=[["A_pi","mu0","beta_e","q_base","q_nmsi","saving_pct"]]
    for A in A_pis:
        for m in mu0s:
            for b in betas:
                q0, qN, s = run_case(A, m, b)
                rows.append([A, m, b, q0, qN, s])
    with open("param_sweep_results.csv","w",newline="") as f:
        csv.writer(f).writerows(rows)
    print("Wrote param_sweep_results.csv")
