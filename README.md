# NMSI Two-Flux Model (Active + Passive, Co-directional)

This folder contains a minimal **two-flux** demonstration under the NMSI framework (π*, γ_diss, e*),
for **interpenetrating co-directional flows**: an **active** driver A and an **entrained** passive flow P.

> Version: 2025-09-27

## What is here
- `twoflux_nmsi_1d_timeseries.csv`: 1D adaptation solution for the passive flow `u_P(x)` with coupling and NMSI operators.
- `figures/`:
  - `flux_velocities.png`: velocity profiles (u_A, u_P) and relative mismatch w.
  - `energy_dissipation.png`: energy proxy vs. CME-like stress and γ_diss gate.
  - `observables.png`: tail-language observables (deflection θ, brightness, bifurcation index).

## Governing 1D equation (demo)
We integrate along x:
```
du_P/dx = (kappa/(rho_P*U_A))*(U_A - u_P)
          - (lambda_e/U_A)*u_P
          - (gamma_diss(x)/U_A)*u_P
          + pi_star(x)/(rho_P*U_A)
```
where:
- **π*** = oscillatory forcing,
- **γ_diss** = selective dissipation (Z-window gating),
- **e*** = exponential stabilizer (here `lambda_e`).

## How to use
1. Drop this folder into your repo (e.g., `NMSI-NavierStokes/twoflux_model/`).
2. Plot the CSV or reproduce the figures.
3. Replace the synthetic `stress(x)` with real CME proxies (|B|, V_sw, Kp mapped to distance/time).

## Next steps
- Extend to **2D pseudo-spectral**, apply γ_diss(k) per band.
- Fit {"π*", "γ_diss", "e*"} to real comet-tail observations (θ, brightness, bifurcation timing).
- Publish the **CME–Comet Oscillatory Dialogue** as a formal NMSI case study.
