# benchmarks/bare_slab/run_benchmark.py
"""
Benchmark 1: Bare Homogeneous Slab Reactor
Compare PyReactor k-eff vs analytical 2-group formula
"""
import sys, os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'pyreactor'))

from materials import Material, MaterialLibrary
from geometry  import Mesh1D
from solver_1d import DiffusionSolver1D

# ── Cross sections (pure fuel, no reflector) ──────────────────
D1        = 1.40
D2        = 0.37
sigma_a1  = 0.0095
sigma_a2  = 0.0820
sigma_s12 = 0.0210
nu_sf1    = 0.0060
nu_sf2    = 0.1350

# ── Geometry ──────────────────────────────────────────────────
L         = 160.0       # bare fuel slab width (cm)
n_nodes   = 200

# ─────────────────────────────────────────────────────────────
# ANALYTICAL SOLUTION
# ─────────────────────────────────────────────────────────────
# Extrapolated length correction for vacuum BC
# Standard approximation: add 2 × D to each side
h_bench = L/n_nodes          # extrapolated length for group 1
L_eff  = L+h_bench

# Geometric buckling
B2 = (np.pi / L_eff)**2

print(f"  Mesh spacing     : {h_bench:.4f} cm")
print(f"  Extrapolated L   : {L_eff:.4f} cm")
print(f"  Buckling B²      : {B2:.8f} cm⁻²")

# Group 1 removal
sigma_r1 = sigma_a1 + sigma_s12

# 2-group criticality formula
numerator   = nu_sf1 * (D2*B2 + sigma_a2) + nu_sf2 * sigma_s12
denominator = (D1*B2 + sigma_r1) * (D2*B2 + sigma_a2)
k_analytical = numerator / denominator

print("\n" + "="*55)
print("  Benchmark 1: Bare Homogeneous Slab")
print("="*55)
print(f"  Slab width       : {L} cm")
print(f"  Extrapolated L   : {L_eff:.4f} cm")
print(f"  Buckling B²      : {B2:.6f} cm⁻²")
print(f"  k (analytical)   : {k_analytical:.6f}")

# ─────────────────────────────────────────────────────────────
# PYREACTOR NUMERICAL SOLUTION
# ─────────────────────────────────────────────────────────────
lib = MaterialLibrary()
fuel = Material("fuel", D1=D1, D2=D2,
                sigma_a1=sigma_a1, sigma_a2=sigma_a2,
                sigma_s12=sigma_s12,
                nu_sigma_f1=nu_sf1, nu_sigma_f2=nu_sf2)
lib.add_material(fuel)

regions = [{'start': 0.0, 'end': L, 'material': 'fuel'}]
mesh    = Mesh1D(L, n_nodes, regions, lib)
solver  = DiffusionSolver1D(mesh)
k_numerical, _ = solver.solve()

# ─────────────────────────────────────────────────────────────
# COMPARISON
# ─────────────────────────────────────────────────────────────
error_pcm = abs(k_numerical - k_analytical) / k_analytical * 1e5

print(f"  k (PyReactor)    : {k_numerical:.6f}")
print(f"  Difference       : {abs(k_numerical-k_analytical):.6f}")
print(f"  Error            : {error_pcm:.1f} pcm")
print("-"*55)

if error_pcm < 200:
    print("  ✅ BENCHMARK PASSED  (error < 200 pcm)")
elif error_pcm < 500:
    print("  ⚠️  ACCEPTABLE       (error < 500 pcm)")
else:
    print("  ❌ BENCHMARK FAILED  (error > 500 pcm)")
print("="*55)