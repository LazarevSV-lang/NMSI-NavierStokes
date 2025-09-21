# 🧮 NMSI Diagnostics Notebook

This Jupyter notebook provides ready-to-use diagnostics for simulations under the  
**NMSI–π*–HDQG augmented Navier–Stokes framework**.

## 📌 Features
- Compare **Classical NSE vs Augmented NMSI** runs
- Plot:
  - Energy **E(t)**
  - Enstrophy **Ω(t)**
  - Max vorticity **‖ω‖∞**
  - Energy spectrum **E(k)**
- Estimate **Lyapunov exponent λ_max** via twin trajectories

## 🚀 How to Run
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch Jupyter:
   ```bash
   jupyter notebook NMSI_Diagnostics_Notebook.ipynb
   ```
3. Replace file paths in the notebook with your simulation outputs:
   - `out_classical/final_timeseries.npz`
   - `out_augmented/final_timeseries.npz`

## 📂 Input Data
The notebook expects `.npz` or `.csv` files with at least:
- `t` (time array)
- `E` (energy)
- `Omega` (enstrophy)
- `wmax` (optional: max vorticity)

For spectra:  
`spectrum_Ek.npz` with fields `k`, `Ek`.

## 📊 Example Workflow
- Run 64³ shakeout (ν=5e-4) with Classical & Augmented configs
- Load outputs in notebook
- Generate comparison plots
- Run Lyapunov analysis (base vs perturbed trajectory)
- Share results for community validation

## 🔬 Citation
If you use this notebook, please cite:

Lazarev, S. V. (2025).  
*Solving the Millennium Problem — Navier–Stokes Regularity Under the Poincaré–Perelman_NMSI_π*–HDQG Framework.*  
Zenodo. https://doi.org/10.5281/zenodo.17163066
