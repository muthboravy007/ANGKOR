# PyReactor - Physics Theory

## 1. The Neutron Diffusion Equation 

PyReactor solves the steady-state 2-group neutron diffusion equations. For each energy group g, at every spatial point x, we define 

$$-D_g\cdot \frac{d^2\Phi_g}{dx^2} +\Sigma_{r,g}\cdot \Phi_g = S_g$$

Where: 

    - $\Phi_g$  = neutron flux in group $g$   $(n/cm^2\cdot s)$

    - $D_g$     = diffusion coefficient (cm)

    - $\Sigma_{r,g}$    = removal cross section $(cm^{-1})$

    - $S_g$     = neutron source in group $g$. 

## 