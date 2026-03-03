# MCNP Benchmark — Moderated UO2 Slab

## Problem Description
Homogeneous mixture of UO2 (30 vol%) and H2O (70 vol%)
Bare slab, 160 cm width, vacuum boundary conditions
UO2: 3.1% enriched, density 10.4 g/cm³
Mixed density: 3.82 g/cm³

## Results

| Code | Method | k-eff | Uncertainty |
|---|---|---|---|
| MCNP 6.2 | Continuous-energy Monte Carlo | 1.32811 | ±0.00028 |
| PyReactor | 2-group diffusion (textbook XS) | 1.30866 | — |
| **Difference** | | **1,464 pcm** | |

## Fission Spectrum (MCNP)
- Thermal (<0.625 eV): 84.87%
- Epithermal: 9.56%  
- Fast (>100 keV): 5.57%

## Discussion
The 1,464 pcm difference is expected and explained by:
1. Textbook 2-group XS vs ENDF/B-VIII.0 nuclear data
2. 2-group energy discretization vs continuous energy
3. Homogenization approximation

To reduce this difference to <200 pcm, group constants
should be generated from MCNP flux-weighted reaction
rates (cross section homogenization) — planned for v1.2.

## MCNP Input
See bare_slab.i and moderated_slab.i in this folder.