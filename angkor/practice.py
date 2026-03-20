import h5py 
import numpy as np 

# create a simple HDF5 file 
with h5py.File("test.h5", "w") as f: 
    # great a group call "U235"
    g = f.create_group("u235")
    
    # Store an energy arrary inside it 
    E = np.logspace(-5,7,10000)
    sig_f   = 580.0/ np.sqrt(E/0.0253)          # fission XS
    sig_a   = 620.0/ np.sqrt(E/0.0253)
    phi     = 1.0/E                             # 1/E solving down spectrum
    
    # 2-Group boundaries (eV)
    E_boundary  = 0.625
    
    # Group 1: Fast (E>0.625)
    mask_g1 = E> 0.625
    E_g1    = E[mask_g1]
    sig_f_g1= sig_f[mask_g1]
    phi_g1  = phi[mask_g1]
    
    # Flx-weighted avaerage using trapezoidal integration
    numer_g1 = np.trapezoid(sig_f_g1*phi_g1,E_g1)
    denom_g1 = np.trapezoid(phi_g1,E_g1)
    
    sig_f_avg_g1    = numer_g1/denom_g1
    
    # Group 2: Thermal (E<0.625)
    mask_g2 = E<0.625
    E_g2    = E[mask_g2]
    sig_f_g2= sig_f[mask_g2]
    phi_g2  = phi[mask_g2]
    
    # Flx-weighted avaerage using trapezoidal integration
    numer_g2 = np.trapezoid(sig_f_g2*phi_g2,E_g2)
    denom_g2 = np.trapezoid(phi_g2,E_g2)
    
    sig_f_avg_g2    = numer_g2/denom_g2
    
    print(f"Group 1 (fast)    sig_f = {sig_f_avg_g1:.4f} barns")
    print(f"Group 2 (thermal) sig_f = {sig_f_avg_g2:.4f} barns")
    print(f"Ratio G2/G1 = {sig_f_avg_g2/sig_f_avg_g1:.1f}x")
    
    g.create_dataset("energy", data=E)
    g.create_dataset("fission", data=sig_f)
    g.create_dataset("absorb", data=sig_a)
    
    
# Read it back 
with h5py.File("test.h5", "r") as f: 
    g       = f["u235"]
    E       = g["energy"][:]
    sig_f   = g["fission"][:]
    sig_a   = g["absorb"][:]
    
    # Check value at thermal energy (E = 0.0253 eV)
    # Find index closest to 0.0253 eV 
    thermal_idx = np.argmin(np.abs(E-0.0253))

print(f"At thermal energy (E = {E[thermal_idx]:.4f} eV):")
print(f"  Fission XS  : {sig_f[thermal_idx]:.2f} barns")
print(f"  Absorption XS: {sig_a[thermal_idx]:.2f} barns")
