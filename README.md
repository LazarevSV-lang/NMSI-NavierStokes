# NMSI Navier–Stokes Snippet

This package contains a minimal demonstration of the **NMSI–π*–γ_diss–e*** solver modification
for Navier–Stokes equations.

## Files
- `nmsi_solver.py` — step function with π*, γ_diss, e* operators.
- `diagnostics.py` — helper functions for energy, enstrophy, max vorticity.
- `README.md` — this file.

## Usage
Integrate `step` into a pseudo-spectral Navier–Stokes solver with FFT, nonlinear terms, and projection.
Then use the diagnostics to track stability improvements.
