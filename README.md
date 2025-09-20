# NMSI–π*–HDQG Augmented Navier–Stokes — Simulation Starter

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI: Zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.17163066.svg)](https://zenodo.org/records/17163066)

Simulation framework for **augmented Navier–Stokes equations** under the  
**Poincaré–Perelman_NMSI_π*–HDQG** model.  
It introduces:
- **π*** cyclic forcing (bounded oscillatory input),
- **γ_diss** intermittent dissipation (Z-windows),
to guarantee bounded energy and enstrophy, excluding singularities.

This work supports the preprint:  
📄 *Solving the Millennium Problem — Navier–Stokes Regularity Under the Poincaré–Perelman_NMSI_π*–HDQG Framework*  
👉 [Zenodo, 2025](https://zenodo.org/records/17163066)

---

## 📂 Repository contents
- `nmsi_nse3d_tg.py` — 3D pseudo-spectral skeleton (Taylor–Green vortex, vortex stretching).
- `nmsi_nse2d_demo.py` — 2D finite-difference demo (quick boundedness check).
- `config.yaml` — central configuration file (grid, ν, CFL, π*, γ_diss).
- `demo_plots.ipynb` — notebook to visualize Energy E(t), Enstrophy Ω(t), Max Vorticity.
- `PARAMETERS.md` — advanced guide for parameter tuning.
- `LICENSE` — MIT License.
- `CITATION.cff` — citation metadata.
- `RELEASE_NOTES.md` — release notes.
- `requirements.txt` — Python dependencies.

---

## ⚙️ Installation
```bash
git clone https://github.com/LazarevSV-lang/NMSI-NavierStokes.git
cd NMSI-NavierStokes
pip install -r requirements.txt
```

Requirements: Python ≥3.8, NumPy, PyYAML, Matplotlib.

---

## 🚀 Usage

### 3D pseudo-spectral run
```bash
python nmsi_nse3d_tg.py --config config.yaml
```
Diagnostics are saved as `.npz` in `out_3d/`.

### 2D quick demo
```bash
python nmsi_nse2d_demo.py --config config.yaml
```
This generates `out_2d_diag.csv`.

Then visualize with:
```bash
jupyter notebook demo_plots.ipynb
```

---

## 📊 Diagnostics
- **Energy** E(t)  
- **Enstrophy** Ω(t)  
- **Max vorticity** ‖ω‖∞  

PASS = bounded quantities + stable spectra.

---

## ⚙️ Advanced configuration
For details on how to tune parameters in `config.yaml`  
(for longer runs, turbulence intensity, and comparison with classical NSE),  
see the full guide here: [PARAMETERS.md](PARAMETERS.md)

---

## 📖 Citation
If you use this code, please cite:

```
Lazarev, S. V. (2025).
Solving the Millennium Problem — Navier–Stokes Regularity Under the Poincaré–Perelman_NMSI_π*–HDQG Framework.
Zenodo. https://doi.org/10.5281/zenodo.17163066
```

---

## 🔬 Open Peer Review
This repository is part of an **open peer review** process.  
Experts are invited to analyze the derivations, run simulations, and test predictions.  
Feedback and contributions are highly welcome!

#NavierStokes #MillenniumProblem #NMSI #HDQG #OpenScience
