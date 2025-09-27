# NMSI OpenFOAM Integration

This package provides two baseline test cases (`flatPlate_M7` and `sphereCone_M8`) for testing the NMSI-π*-γ_diss-e* framework inside OpenFOAM using `rhoCentralFoam`.

### Contents
- `fvOptions`: adds codedSource forcing with π* and e* operators
- `controlDict`: includes wall heat flux and Cp monitors
- Directories `0/` and `constant/` are placeholders (fill with IC/BC and mesh)

### How to Run
1. Copy one test case (e.g. `flatPlate_M7`) into your OpenFOAM run directory.
2. Add appropriate initial and boundary conditions to `0/` and mesh to `constant/`.
3. Run:
   ```bash
   rhoCentralFoam
   ```
4. Post-process using wall heat flux and Cp outputs.

### Notes
- γ_diss implementation not fully coded here; extend via selective viscosity boost.
- This is a prototype skeleton, not a full validated setup.
