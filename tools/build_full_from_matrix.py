from pathlib import Path

mat = [
['R','R','R','R','R','R','R','R','R','R','R','R','R','R','R','R','R'],
['R','R','R','R','R','R','R','R','R','R','R','R','R','R','R','R','R'],
['R','R','R','R','R','R','R','R','R','R','R','R','R','R','R','R','R'],
['R','R','R','R','R','R','R','R','F2','F1','F1','F2','R','R','R','R','R'],
['R','R','R','R','R','R','R','R','R','F1','F2','F1','R','R','R','R','R'],
['R','R','R','CR','F2','F2','F1','F1','F2','F1','F1','F2','F2','CR','R','R','R'],
['R','R','R','CR','F2','F2','F1','F1','F1','F1','F1','F2','F2','CR','R','R','R'],
['R','R','R','F2','F2','F1','F1','F1','F1','F1','F1','F1','F1','F2','F2','R','R'],
['R','R','F2','F2','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F2','F2','R'],
['R','F2','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F2','R'],
['R','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','R'],
['R','F2','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F2','R'],
['R','R','F2','F2','F1','F1','F1','F1','F1','F1','F1','F1','F1','F1','F2','F2','R'],
['R','R','R','F2','F2','F1','F1','F1','F1','F1','F1','F1','F1','F2','F2','R','R'],
['R','R','R','CR','F2','F2','F1','F1','F1','F1','F1','F2','F2','CR','R','R','R'],
['R','R','R','R','CR','F2','F2','F1','F1','F2','F2','F1','F1','R','R','R','R'],
['R','R','R','R','R','F2','F2','F1','F1','F2','F1','F1','R','R','R','R','R'],
['R','R','R','R','R','R','R','R','F2','F1','F1','F2','R','R','R','R','R'],
]

cell = 10.0
ny = len(mat)
nx = len(mat[0])
name_map = {'R': 'reflector', 'F1': 'fuel1', 'F2': 'fuel2', 'CR': 'fuel_cr'}
regions = []
for j, row in enumerate(mat):
    y_min = j * cell
    y_max = (j + 1) * cell
    for i, val in enumerate(row):
        x_min = i * cell
        x_max = (i + 1) * cell
        regions.append(
            f"  - {{name: r{ny - j}c{i + 1}, x_min: {x_min:.1f}, x_max: {x_max:.1f}, y_min: {y_min:.1f}, y_max: {y_max:.1f}, material: {name_map[val]} }}"
        )

materials_block = '''materials:
  fuel1:
    groups: 2
    D: [1.5, 0.4]
    sigma_a: [0.0100, 0.0850]
    nu_sigma_f: [0.0000, 0.135]
    chi: [1.0, 0.0]
    sigma_s:
      - [0.0, 0.0200]
      - [0.0, 0.0]

  fuel2:
    groups: 2
    D: [1.5, 0.4]
    sigma_a: [0.0100, 0.1300]
    nu_sigma_f: [0.0000, 0.135]
    chi: [1.0, 0.0]
    sigma_s:
      - [0.0, 0.0200]
      - [0.0, 0.0]

  fuel_cr:
    groups: 2
    D: [1.5, 0.4]
    sigma_a: [0.0100, 0.1800]
    nu_sigma_f: [0.0000, 0.135]
    chi: [1.0, 0.0]
    sigma_s:
      - [0.0, 0.0200]
      - [0.0, 0.0]

  reflector:
    groups: 2
    D: [2.0, 0.3]
    sigma_a: [0.0000, 0.0100]
    nu_sigma_f: [0.0, 0.0]
    chi: [0.0, 0.0]
    sigma_s:
      - [0.0, 0.0400]
      - [0.0, 0.0]
'''

solver_block = '''solver:
  max_iterations: 1000
  convergence: 1.0e-6
  buckling: 8.0e-5
'''

bc_block = '''boundary_conditions:
  left: vacuum
  right: vacuum
  top: vacuum
  bottom: vacuum
'''

lines = []
lines.append('title: "IAEA 2D PWR Benchmark Full Core"')
lines.append('geometry:')
lines.append('  type: 2D_rectangular')
lines.append(f'  domain_x: {nx*cell}')
lines.append(f'  domain_y: {ny*cell}')
lines.append(f'  nx: {nx}')
lines.append(f'  ny: {ny}')
lines.append('regions:')
lines.extend(regions)
lines.append(materials_block.rstrip())
lines.append(solver_block.rstrip())
lines.append(bc_block.rstrip())
Path('input/iaea_2d_full.yaml').write_text('\n'.join(lines)+'\n')
print('Wrote input/iaea_2d_full.yaml with', len(regions), 'regions')
