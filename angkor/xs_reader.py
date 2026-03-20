import numpy as np 
import h5py 
import os 

class XSReader:
    '''Reads HDF5 nuclear data and condenses to few groups'''
    Groups_Structure = {
        "2-group": [2.0e7, 6.25e-1, 1.0e-5],
        "4-group": [2.0e7, 8.12e5, 5.53e3, 6.25e-1, 1.0e-5]
    }
    
    def __init__(self, filepath):
        self.filepath = filepath 
        
    def read_nuclide(self, nuclide):
        '''REad continous XS for one nuclide from HDF5'''
        with h5py.File(self.filepath, "r") as f:
            g = f[nuclide]
            data = {
                "energy"    : g["energy"][:],
                "fission"   : g["fission"][:],
                "absorb"    : g["absorb"][:]
            }
        print(f"  Read {nuclide}: {len(data['energy'])} points")
        print(f"  E range: {data['energy'][0]:.2e} to {data['energy'][-1]:.2e}")
        return data 
    
    def condense(self, nuclide_data, groups_structure="2-group"):
        '''
        Condense continous XS to few-group constants. 
        Uses flux-weighted average with 1/E specturm.
        '''
        boundaries  = self.Groups_Structure[groups_structure]
        G           = len(boundaries)- 1
        
        E           = nuclide_data["energy"]
        sig_f       = nuclide_data["fission"]
        phi         = 1.0/E 
        
        results     = []
        
        for g in range(G):
            E_max   = boundaries[g]
            E_min   = boundaries[g+1]
            
            mask    = (E>=E_min) & (E<=E_max)
            print(f"Group {g}: E_min={E_min:.2e}, E_max={E_max:.2e}")
            print(f"  Points in group: {np.sum(mask)}")
            
            E_g     = E[mask]
            sig_f_g = sig_f[mask]
            phi_g   = phi[mask]
            
            # FLux-weighted average
            numer   = np.trapezoid(sig_f_g*phi_g,E_g)
            denom   = np.trapezoid(phi_g, E_g)
            print(f"  numer={numer:.4e}, denom={denom:.4e}")
            
            sig_f_avg   = numer/denom if denom > 0 else 0.0 
            results.append(sig_f_avg)
            
        return results 
    
if __name__ == "__main__":
    reader = XSReader("test.h5")
    data   = reader.read_nuclide("u235")
    xs_2g  = reader.condense(data, "2-group")
    xs_4g  = reader.condense(data, "4-group")

    print("2-group sig_f:", [f"{x:.2f}" for x in xs_2g])
    print("4-group sig_f:", [f"{x:.2f}" for x in xs_4g])    
            
            
        