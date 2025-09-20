# 🔧 Parameter Guide — NMSI–π*–HDQG Navier–Stokes (config.yaml)

## 1) Grid & domain
```yaml
grid:
  nx: 64
  ny: 64
  nz: 64
  Lx: 6.283185307
  Ly: 6.283185307
  Lz: 6.283185307
```
- Increase resolution (`nx,ny,nz`) for longer/more turbulent runs (96–128³).
- Reduce `dt_max` or CFL if needed.

## 2) Physics (viscosity)
```yaml
physics:
  nu: 1.0e-3
```
- Lower `nu` → more turbulence (requires higher resolution).

## 3) Time & stability
```yaml
time:
  t_end: 2.0
  cfl: 0.4
  dt_min: 1.0e-4
  dt_max: 5.0e-2
  save_every: 10
```
- Increase `t_end` for longer runs (10–20+).
- Lower `cfl` (0.2–0.3) or `dt_max` if unstable.

## 4) π* cyclic forcing
```yaml
forcing_pi:
  use: true
  A_pi: 0.1
  omega_pi: 4.0
  phi: 0.0
  k1: 4.0
  k2: 6.0
  bandpass: true
```
- Increase `A_pi` for stronger forcing.
- Disable with `use: false` to test classical NSE.

## 5) γ_diss intermittent dissipation
```yaml
gamma_diss:
  use: true
  gamma0: 0.05
  omega_Z: 2.0
  phiZ: 0.0
  zeta: 0.0
  spatial_mask: false
```
- Increase `gamma0` for stronger stabilization.
- Adjust `zeta` for more/less active windows.
- Disable with `use: false` for classical NSE.

## 6) Dealiasing (3D)
```yaml
dealias:
  use: true
```
- Keep `true` for high resolution or low viscosity.

---

## 📊 Protocols

### A) Augmented vs Classical NSE
1. Augmented: `forcing_pi.use=true`, `gamma_diss.use=true`
2. Classic: `forcing_pi.use=false`, `gamma_diss.use=false`
3. Same grid/nu/t_end → compare E(t), Ω(t), ‖ω‖∞

### B) Long-run robustness
- `t_end: 20.0`, `cfl: 0.3`, `dt_max: 0.02`
- Increase resolution if `nu <= 5e-4`

### C) Reproducibility
- Record all key params + output series (`out_3d/*.npz`, `out_2d_diag.csv`).

---

## 🧰 Practical tips
- If `‖ω‖∞` blows up → lower `A_pi`, increase `gamma0`, reduce `cfl`
- If flow dies out → lower `gamma0`, raise `zeta`, reduce `nu`
- For 3D stability → replace Euler with RK2/RK3 (planned upgrade)
