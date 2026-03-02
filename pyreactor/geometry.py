import numpy as np 
from materials import MaterialLibrary, Material

class Mesh1D:
    def __init__(self, total_length, n_nodes, regions, material_library):
        """_summary_

        Args:
            total_length (float): total reactor length in cm
            n_nodes (int): number of mesh nodes
            regions (list of dicts): each dict has {'start':0, 
                                    'end':20, 'material':'water'}
            material_library (object): MaterialLibrary
        """
        self.total_length   = total_length
        self.n_nodes        = n_nodes
        self.regions        = regions
        self.lib            = material_library
        self.h              = total_length/n_nodes
        
        # Build position array: n_nodes points from h/2 to L-h/2
        # cell-centered: first node at h/2, last node at L-h/2 
        self.x = np.linspace(self.h/2, self.total_length-self.h/2, self.n_nodes)
        self._build_xs_arrays()
    
    def _build_xs_arrays(self):
        n = self.n_nodes 
        self.D1 = np.zeros(n)
        self.D2 = np.zeros(n)
        self.sigma_a1   = np.zeros(n)
        self.sigma_a2   = np.zeros(n)
        self.sigma_s12  = np.zeros(n)
        self.nu_sf1     = np.zeros(n)
        self.nu_sf2     = np.zeros(n)
        
        # Loop over each node
        for i in range(n):
            xi = self.x[i]                  # position of node i 
            mat = self._get_material_at(xi) # find which material it is
            
            # Assign cross sections from material to arrays 
            self.D1[i] = mat.D1
            self.D2[i] = mat.D2 
            self.sigma_a1[i]  = mat.sigma_a1
            self.sigma_a2[i]  = mat.sigma_a2
            self.sigma_s12[i] = mat.sigma_s12
            self.nu_sf1[i]    = mat.nu_sigma_f1
            self.nu_sf2[i]    = mat.nu_sigma_f2
            
    def _get_material_at(self, x):
        ''' Return the material object for position x.'''
        # print(f"DEBUG: check x = {x:.4f}")
        for region in self.regions:
            # print(f" region: {region['start']} to {region['end']}")
            if region['start'] <= x < region['end']:
                name = region['material']
                return self.lib.get_material(name)
        last = self.regions[-1]
        if x<= last['end']:
            return self.lib.get_material(last['material'])
        
        raise ValueError(f"Position x = {x:.4f} cm not fount in any region!")
        
    def summary(self):
        """ Print a summary of the mesh."""
        print(f"1D Mesh Summary")
        print(f"   Total Length: {self.total_length} cm")
        print(f"   Node: {self.n_nodes}")
        print(f"   Mesh spacing: {self.h:.4f} cm")
        print(f"   x range: {self.x[0]:.3f} → {self.x[-1]:.3f} cm")
        print(f"   Regions: {len(self.regions)}")
        
if __name__ == "__main__":
    import matplotlib.pyplot as plt 
    from materials import Material, MaterialLibrary
    
    lib = MaterialLibrary()
    
    uo2 = Material("uo2_fuel", D1=1.40, D2=0.37,
                   sigma_a1=0.0095, sigma_a2=0.0820,
                   sigma_s12=0.0210, nu_sigma_f1=0.0060, nu_sigma_f2=0.1350)

    water = Material("water", D1=1.13, D2=0.16,
                     sigma_a1=0.0003, sigma_a2=0.0210,
                     sigma_s12=0.0460, nu_sigma_f1=0.0, nu_sigma_f2=0.0)

    lib.add_material(uo2)
    lib.add_material(water)
        
    # Step 2: Define regions
    regions = [
        {'start':   0.0, 'end':  20.0, 'material': 'water'},
        {'start':  20.0, 'end': 180.0, 'material': 'uo2_fuel'},
        {'start': 180.0, 'end': 200.0, 'material': 'water'},
    ]
    
    # Step 3: Build mesh
    mesh = Mesh1D(total_length=200.0, n_nodes=200,
                  regions=regions, material_library=lib)
    mesh.summary()

    # Step 4: Plot D1 across the reactor — should show 3 zones clearly
    plt.figure(figsize=(10, 4))
    plt.plot(mesh.x, mesh.D1, color='steelblue', linewidth=2)
    plt.xlabel("Position x (cm)")
    plt.ylabel("D1 (cm)")
    plt.title("Fast Diffusion Coefficient Across Reactor")
    plt.axvline(x=20,  color='red', linestyle='--', label='fuel start')
    plt.axvline(x=180, color='red', linestyle='--', label='fuel end')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()