# 📊 NMSI Diagnostics Demo Package

This package contains a **Jupyter notebook** and a **synthetic demo dataset** for testing the  
NMSI–π*–HDQG augmented Navier–Stokes framework.

## 📂 Contents
- `NMSI_Diagnostics_Notebook_Demo.ipynb` — Notebook with fallback to demo dataset
- `demo_timeseries.npz` — Synthetic dataset (Energy, Enstrophy, Max Vorticity)

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch Jupyter:
   ```bash
   jupyter notebook NMSI_Diagnostics_Notebook_Demo.ipynb
   ```
3. If no simulation outputs are found in `out_classical/` or `out_augmented/`,  
   the notebook will automatically load the demo dataset.

## 📊 Demo Dataset
The synthetic dataset includes:
- `t` (time array, 0–20, 200 points)
- `E_classical`, `E_augmented`
- `Omega_classical`, `Omega_augmented`
- `wmax_classical`, `wmax_augmented`

## 🔬 Citation
If you use this notebook or dataset, please cite:

Lazarev, S. V. (2025).  
*Solving the Millennium Problem — Navier–Stokes Regularity Under the Poincaré–Perelman_NMSI_π*–HDQG Framework.*  
Zenodo. https://doi.org/10.5281/zenodo.17163066
