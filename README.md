# NMSI–π*–HDQG Augmented Navier–Stokes — Simulation Starter (v2)

This kit shows how bounded cyclic forcing (π*) and intermittent dissipation (γ_diss) stabilize flows and suppress blow‑up.

**Contents**
- `nmsi_nse3d_tg.py` — 3D pseudo‑spectral skeleton (Taylor–Green vortex; vortex stretching test).
- `nmsi_nse2d_demo.py` — 2D finite‑difference demo (quick energy/enstrophy validation).
- `config.yaml` — central parameters (grid, ν, CFL, π* forcing, γ_diss windows).
- `README.md` — how to run & diagnostics.

**Model**
∂_t u + (u·∇)u = −∇p + νΔu + F_{π*}(x,t) − γ_diss(x,t) u,   ∇·u=0

F_{π*}(k,t) = A_π cos(ω_π t + φ) 𝔅(k;k1,k2) û(k,t) (bounded, band‑limited)
γ_diss(t) = { γ0  if sin(ω_Z t + φ_Z) > ζ ; 0 otherwise }  (coercive windows)

**Diagnostics**
- Energy E(t), Enstrophy Ω(t), Max vorticity ||ω||_∞
- Energy budget & CFL (optional), spectra (optional)

**PASS/FAIL**
Bounded E(t), bounded Ω(t), no explosive ||ω||_∞, small energy‑balance residuals.

**Run**
3D: `python nmsi_nse3d_tg.py --config config.yaml`
2D: `python nmsi_nse2d_demo.py --config config.yaml`
