# ReentryBluntBody_NMSI (OpenFOAM case)

Axisymmetric blunt-body wedge case for the **rhoCentralFoamNMSI** solver.
Includes NMSI operators (π*, γ_diss with Z-window, e* clamp).

## Run
```
blockMesh
rhoCentralFoamNMSI
```

## Notes
- Adjust inlet total pressure/temperature to match target Mach/Re (use tunnel data).
- Strengthen shock masking (gammaDiss.shockMaskC) if π* interacts with the bow shock.
- Validate shock standoff distance, stagnation heat flux, and Cp(θ) against experiment.
