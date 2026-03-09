import numpy as np 
from scipy import linalg

def build_group_matrix(D_arr, sigma_r_arr, h):
    """_summary_
    
    Build the NxN loss matrix for one energy group. 

    Args:
        D_arr (array)       : array of diffusion coefficient at each node
        sigma_r_arr (array) : array of REMOVAL cross section at each node
        h (float)           : mesh spacing
        
    returns: NxN numpy matrix
    """
    N = len(D_arr)
    L = np.zeros((N,N))     # Start with all zero
    
    for i in range(N):
        D = D_arr[i]
        # Diagonal term
        if i == 0 or i == N-1:
            L[i,i] = D/h**2 + sigma_r_arr[i]    # boundary condition
        else:
            # interior node - two neighbors
            L[i,i] = 2*D/h**2 + sigma_r_arr[i]
        
        # off-diagonal terms
        if i>0:
            D_left      = (D[i]+D[i-1])/2
            L[i,i-1]    = -D_left / h**2 
        if i< N-1:
            D_right     = (D[i]+D[i-1])/2
            L[i,i+1]    = -D_right/h**2 
    return L 

class DiffusionSolver1D:
    def __init__(self, mesh):
        """mesh: a Mesh1D object (from geometry.py)"""
        self.mesh   = mesh 
        self.N      = mesh.n_nodes
        self.h      = mesh.h 
        
    def build_matrices(self):
        """Build the fuell 2N x 2N L and F matrices"""
        N = self.N 
        mesh = self.mesh 
        
        # --- Build L1: Group 1 loss matrix ---
        sigma_r1 = mesh.sigma_a1 + mesh.sigma_s12   # removal = absorption + scattering out
        L1 = build_group_matrix(mesh.D1, sigma_r1, self.h)
        
        # --- Build L2: Group 2 loss matrix ---
        sigma_r2 = mesh.sigma_a2                         
        L2 = build_group_matrix(mesh.D2, sigma_r2, self.h)
        
        # --- Build scattering block: -Σ_s12 on diagonal ---
        S12 = np.diag(-mesh.sigma_r_arr)            # hint: sigma_s12 array
        
        # --- Assemble full 2N x 2N L matrix ---
        # Block structure:
        # [L1    |  0  ]
        # [S12   |  L2 ]
        self.L = np.zeros((2*N, 2*N))
        self.L[0:N,   0:N]  = L1        # top-left block
        self.L[N:2*N, 0:N]  = S12       # bottom-left block  
        self.L[N:2*N, N:2*N]= L2        # bottom-right block
        
        # --- Build full 2N x 2N F matrix ---
        # Block structure:
        # [νΣ_f1 | νΣ_f2]
        # [  0   |   0  ]
        self.F = np.zeros((2*N, 2*N))
        self.F[0:N, 0:N]  = np.diag(mesh.nu_sf1)    # hint: nu_sf1
        self.F[0:N, N:2*N]= np.diag(mesh.nu_sf2)    # hint: nu_sf2
        
        return self.L, self.F
    
    def solve(self, max_iter=1000, tol=1e-6):
        """
        Power iteration to find k-eff and flux.
        Returns: k (float), phi (array of length 2N)
        """
        N = self.N
        
        # Step 1: Build matrices
        self.build_matrices()
        
        # Step 2: Initial guess
        phi = np.ones(2*N)         # flat flux guess
        k   = 1.0                  # initial k guess
        
        # Step 3: Power iteration loop
        for iteration in range(max_iter):
            
            # Compute fission source: S = (1/k) * F * phi
            fission_source = (1.0/k) * self.F @ phi
            
            # Solve linear system: L * phi_new = fission_source
            # hint: use np.linalg.solve(A, b)
            phi_new = np.linalg.solve(___, ___)
            
            # Normalize phi_new (prevents numbers growing to infinity)
            phi_new = phi_new / np.max(phi_new)
            
            # Update k using fission rate ratio
            k_new = k * (np.sum(self.F @ phi_new) / 
                         np.sum(self.F @ phi))
            
            # Check convergence
            k_change   = abs(k_new - k)
            phi_change = np.max(np.abs(phi_new - phi))
            
            if k_change < tol and phi_change < tol:
                print(f"  Converged at iteration {iteration+1}")
                print(f"  k-eff = {k_new:.6f}")
                break
            
            # Update for next iteration
            phi = phi_new 
            k   = k_new
        
        # Split flux into two groups
        self.phi1 = phi[0:N]       # fast flux
        self.phi2 = phi[N:2*N]     # thermal flux
        self.k    = k_new
        
        return k_new, phi
    
# Test 
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import sys
    sys.path.insert(0, '.')
    from materials import Material, MaterialLibrary
    from geometry import Mesh1D
    
    # Build the same reactor as before
    lib = MaterialLibrary()
    uo2 = Material("uo2_fuel", D1=1.40, D2=0.37,
                   sigma_a1=0.0095, sigma_a2=0.0820,
                   sigma_s12=0.0210, nu_sigma_f1=0.0060, nu_sigma_f2=0.1350)
    water = Material("water", D1=1.13, D2=0.16,
                     sigma_a1=0.0003, sigma_a2=0.0210,
                     sigma_s12=0.0460, nu_sigma_f1=0.0, nu_sigma_f2=0.0)
    lib.add_material(uo2)
    lib.add_material(water)
    
    regions = [
        {'start':   0.0, 'end':  20.0, 'material': 'water'},
        {'start':  20.0, 'end': 180.0, 'material': 'uo2_fuel'},
        {'start': 180.0, 'end': 200.0, 'material': 'water'},
    ]
    
    mesh = Mesh1D(200.0, 200, regions, lib)
    
    # Solve
    print("Starting power iteration...")
    solver = DiffusionSolver1D(mesh)
    k, phi = solver.solve()
    print(f"\nResult: k-eff = {k:.6f}")
    
    # Plot both group fluxes
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
    
    ax1.plot(mesh.x, solver.phi1, color='red', linewidth=2)
    ax1.set_ylabel("Fast Flux φ₁")
    ax1.set_title(f"2-Group Neutron Flux — k-eff = {k:.6f}")
    ax1.axvline(x=20,  color='gray', linestyle='--')
    ax1.axvline(x=180, color='gray', linestyle='--')
    ax1.grid(True)
    
    ax2.plot(mesh.x, solver.phi2, color='blue', linewidth=2)
    ax2.set_ylabel("Thermal Flux φ₂")
    ax2.set_xlabel("Position x (cm)")
    ax2.axvline(x=20,  color='gray', linestyle='--')
    ax2.axvline(x=180, color='gray', linestyle='--')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()