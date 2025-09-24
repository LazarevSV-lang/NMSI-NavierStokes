# NMSI NSE Notebooks

This bundle provides two Jupyter notebooks for open peer review:

1. **NMSI_NSE3D_TG_skeleton.ipynb**
   - 3D Taylor–Green vortex, pseudo-spectral, SSPRK3
   - Compares classical NSE vs augmented NMSI–π*–γ_diss–e
   - Diagnostics: Energy E(t), Enstrophy Ω(t)
   - Saves results in `out_3d_tg_compare.npz`

2. **NMSI_NSE2D_Compare_ParamSweep.ipynb**
   - 2D pseudo-spectral NSE, parameter sweep
   - Loops over ν, Aπ, ζ, λ_e, α_e values
   - Exports per-case `.npz` and a `summary.csv` with final energy/enstrophy stats

## Usage
Unzip, open notebooks in JupyterLab/Notebook, and run cells. Requires Python 3.x, NumPy, Matplotlib.

Contributions: please fork the repo and submit PRs with additional parameter sweeps, plots, or comparisons.
