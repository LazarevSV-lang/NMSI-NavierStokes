
# NMSI Hypersonic Scout — Stage-A (Mach 6–8 Reentry Glider)

Minimal, testable scaffolding to compare classical vs NMSI-augmented flow metrics
for hypersonic boundary-layer stabilization and heat-flux spike reduction.

## What’s here
- `core/operators.py` — π*, γ_diss (Z-windows), e* and a shock/BL sensor
- `core/heatflux.py`  — Sutton–Graves baseline q̇ correlation (simplified)
- `core/stability.py` — toy energy/enstrophy/spectra functions for diagnostics
- `cases/*.yaml`      — example inputs (Mach 7 flat-plate, Mach 8 sphere-cone)
- `notebooks/*.ipynb` — quick calibration demo
- `tests/`            — sanity test

## Quickstart
```bash
pip install numpy pyyaml
python - << 'PY'
from core.operators import nmsi_glider_step
ops, q0, qN, gain = nmsi_glider_step(
    mach=7.0, t=10.0, aoa_deg=5.0,
    rho_inf=0.015, V_inf=2100.0, Rn=0.05,
    dCp_dx=0.2, div_u=-0.03,
    params={"A_pi":0.35,"w_pi":1.2,"beta_e":0.03,"mu0":0.55,"zeta":6.0},
    Cf_mod=0.35
)
print('qdot_base =', round(q0))
print('qdot_nmsi =', round(qN))
print('gain =', round(float(gain),3))
print('ops =', ops)
PY
```

## Next steps
- Replace toy `stability.py` with real E(t), Ω(t) from CFD or reduced-order solvers.
- Add Fay–Riddell option in `heatflux.py`; couple to wall-temperature models.
- Wire into OpenFOAM/SU2 pre/post to compare Cp(θ), q̇(x) vs NASA datasets.
- Build a small test matrix: AoA, Rn, Tw/T0, chemistry ON/OFF.
