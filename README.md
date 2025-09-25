# Taylor–Green Vortex Benchmark (Classical vs NMSI–π*–γ_diss–e*)

This benchmark runs a **2D pseudo-spectral Taylor–Green** surrogate with toggles for:
- classical NSE,
- π* cyclic forcing,
- γ_diss spectral Z-window,
- e* exponential stabilization.

It produces time series plots for **Energy E(t)**, **Enstrophy Ω(t)**, and **max vorticity**,
and saves raw data to NPZ for reproducibility.

> Note: This is a lightweight 2D surrogate for quick validation on laptops.
> For 3D periodic TG (64³+), mirror the operator toggles in your spectral code (SSPRK3 + 2/3 dealiasing).

## Quick start
```bash
python tg_benchmark.py --nx 64 --ny 64 --nu 1e-3 --t_end 4   --aug on --pi_amp 0.2 --pi_omega 2.0 --e_lambda 0.4 --e_alpha 0.2 --gamma0 0.6
```

Run classical vs augmented and compare outputs in `out/`.

## Files
- `tg_benchmark.py` – main runner (2D pseudo-spectral).
- `plot_results.py` – plot E(t), Ω(t), max|ω| from saved NPZ.
- `config_example.json` – example configuration for reproducibility.
- `LICENSE` – MIT.
