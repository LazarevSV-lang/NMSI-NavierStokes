# FlatPlateHypersonic_NMSI (OpenFOAM case)

A minimal flat-plate hypersonic case wired for the **rhoCentralFoamNMSI** solver
with **π\*** forcing, **γ_diss** (Z-window), and **e\*** clamp via `system/NMSIProperties`.

## Run
```
blockMesh
rhoCentralFoamNMSI
```
(Keep CFL ≤ 0.4; adjust `deltaT` in `system/controlDict` accordingly.)

## Outputs
- `postProcessing/kineticEnergy/...` — integrated kinetic energy.
- `postProcessing/fieldMinMax_vort/...` — min/max vorticity magnitude.

## Notes
- The π* spatial pattern is TG-like; adapt `kx, ky, kz` to your geometry.
- γ_diss is masked in compressive regions (shockMaskC) and gated in time (Z-windows).
- e* provides global exponential stabilization; you can disable it in `NMSIProperties`.
