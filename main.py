import sys 
import yaml 
import os 

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pyreactor'))

from materials import Material, MaterialLibrary
from geometry import Mesh1D
from solver_1d import DiffusionSolver1D
from output import ResultsOutput

def load_input(filepath):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)
    
def run(input_file):
    print(f"\n  PyReactor v1.0")
    print(f"    Input file: {input_file}\n ")
    
    # Step 1: Load input
    data = load_input(input_file)
    
    # Step 2: Build material library
    lib = MaterialLibrary()
    lib.load_from_dict(data['materials'])
    print(f"    Loaded {len(lib.materials)} materials(s):"
          f"{list(lib.materials.keys())}")
    
    # Step 3: Build mesh 
    geom    = data['geometry']
    mesh    = Mesh1D(
        total_length    = geom['length_cm'],
        n_nodes         = geom['mesh_points'],
        regions         = data['regions'],
        material_library = lib 
    )
    print(f"    Build mesh: {mesh.n_nodes} nodes,"
          f"spacing = {mesh.h:.4f} cm")
    
    # Step 4: Solve 
    solver = DiffusionSolver1D(mesh)
    k, phi = solver.solve()
    
    # Step 5: Output
    results     = ResultsOutput(mesh, solver)
    results.print_summary()
    results.plot_flux()
    results.plot_power()
    
if __name__ == "__main__":
    if len(sys.argv) <2:
        input_file = "input/reactor.yaml"
    else:
        input_file = sys.argv[1]
        
    run(input_file)