# Rubin NMSI Testability Notebook

This package contains a Jupyter Notebook designed to be run inside the Rubin Science Platform (RSP).  
It demonstrates how to test **falsifiable predictions** of the NMSI framework using public Rubin data.

## Contents
- `Rubin_NMSI_Testability_Notebook.ipynb`: main notebook with Test A–C implementations.

## Tests Implemented
- **Test A – Galactic vertical-wave harmonics & age-linked phase**
  - Cross-match Gaia DR3 and Rubin data.
  - Search for multiple harmonic structure and phase imprint in young vs. old populations.
- **Test B – Phase synchronization in star-forming regions**
  - Extract Rubin DIA light curves.
  - Compute Kuramoto order parameter R for coherence.
- **Test C – Interstellar Object (ISO) residuals**
  - Identify hyperbolic objects in Rubin Solar System Processing catalogs.
  - Fit residuals, search for quasi-periodic phase structure.

## Falsification Criteria
- No harmonics or phase imprint in Test A weakens NMSI.
- No excess coherence in SFRs in Test B weakens NMSI.
- ISO residuals fully explained by standard models in Test C weakens NMSI.

## How to Use in RSP
1. Log into the [Rubin Science Platform](https://data.lsst.cloud/).
2. Upload or open this notebook inside JupyterLab.
3. Adjust schema/table names if running beyond DP1 (e.g., `dp01_dc2_catalogs` → current schema).
4. Run each section sequentially.
5. Compare outputs against falsification criteria above.

## Notes
- The notebook uses TAP queries (ADQL) and Astropy for analysis.
- Ensure you have network access to Gaia TAP if cross-matching.
- For real ISO residual analysis, integrate with orbital fit packages (e.g., OpenOrb).

---
Author: Generated for NMSI testability demonstration.
