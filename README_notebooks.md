# Notebooks – NMSI–π*–γ_diss–e

This directory hosts analysis notebooks for the augmented Navier–Stokes framework with the exponential operator **e**.

## Files
- `NMSI_NS_e_Notebook_Skeleton.ipynb` – starter notebook to load diagnostics and produce standard plots.

## Environment
- Python ≥ 3.8
- NumPy, SciPy
- Matplotlib
- (Optional) h5py, pandas

Install:
```bash
pip install -r requirements.txt
```

## Data layout
The solvers save diagnostics under `out_3d/` (or `out_2d/`) as `.npz` or `.csv`:
- `timeseries.npz` with keys: `t`, `E`, `Omega`, `wmax`
- Optional spectral snapshots: `snap_k_XXXX.npz` with `k`, `E_k`

## Quick start
1. Place your output files (e.g., `out_3d/timeseries.npz`) in a local path.
2. Open the notebook and set:
```python
path = "out_3d/timeseries.npz"
```
3. Run the cells to generate:
   - Energy E(t)
   - Enstrophy Ω(t)
   - Max vorticity ||ω||∞(t)
   - Energy spectrum E(k) (if snapshots provided)

## Comparative runs
We recommend running three variants with identical resolution and viscosity:
- Baseline NSE
- NSE + π* + γ_diss
- NSE + π* + γ_diss + e (spectral or logistic)

In the notebook, set paths:
```python
paths = {
  "nse": "runs/baseline/timeseries.npz",
  "pi_gamma": "runs/pi_gamma/timeseries.npz",
  "pi_gamma_e": "runs/pi_gamma_e/timeseries.npz"
}
```
The notebook will overlay the curves and report deltas.

## Tuning the e–operator
- Spectral: adjust k_cut, alpha_e, lambda_e to target high-k only.
- Logistic: set beta_E and lambda_e to achieve bounded E(t) without overdamping large scales.

## Expected outcomes
- Bounded E(t) and Ω(t)
- Stable ||ω||∞
- No spectral pile-up at high k
- In HIT, an inertial-range slope close to −5/3

## Reproducibility
- Save the exact config.yaml per run.
- Log random seeds (if any).
- Export final plots (E_vs_t.png, Omega_vs_t.png, wmax_vs_t.png, Ek_spectrum.png).

## Contributing
Open a PR with:
- your config file,
- raw diagnostics,
- plots, and
- a brief summary of observations.

We welcome community tests at different Reynolds numbers, grids, and both spectral and logistic e–operator variants.
