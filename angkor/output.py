import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.gridspec as girdspec 
from datetime import datetime

class ResultsOutput:
    def __init__(self, mesh, solver):
        """_summary_

        Args:
            mesh (_type_): Mesh1D object
            solver (_type_): DiffusionSolver1D object (after solve() has been called)
        """
        
        self.mesh       = mesh 
        self.solver     = solver 
        self.x          = mesh.x 
        
        # compute power distribution 
        self.power = (mesh.nu_sf1 * solver.phi1 + mesh.nu_sf2 * solver.phi2)
        
        # Normalize: peak power = 1.0
        self.power_normalized = self.power / np.max(self.power)
    
    def print_summary(self):
        """Print a clean results tables to terminal."""
        
        print("\n" + "="*55)
        print("          PyReactor - Result Summary")
        print("="*55)
        print(f"    Data/Time           : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"    Geometry            : 1D Slab")
        print(f"    Reactor Length      : {self.mesh.total_length} cm")
        print(f"    Mesh nodes          : {self.mesh.n_nodes}")
        print(f"    Mesh spacing        : {self.mesh.h:.4f} cm")
        print(f"-"*55)
        print(f"    k-eff               : {self.solver.k:.6f}")
        
        # Reactivity in pcm (standard industry unit)
        # rho = (k-1)/k*100000 pcm 
        rho = (self.solver.k - 1.0)/self.solver.k*1e5
        print(f"    Reactivity          : {rho:+.1f} pcm")
        print(f"-"*55)
        
        # Peak flux location
        peak_fast       = self.x[np.argmax(self.solver.phi1)]
        peak_thermal    = self.x[np.argmax(self.solver.phi2)]
        peak_power      = self.x[np.argmax(self.power_normalized)]
        
        print(f"    Peak fast flux at x     = {peak_fast:.1f} cm")
        print(f"    Peak thermal flux at x  = {peak_thermal:.1f} cm")
        print(f"    Peak power at x         = {peak_power:.1f} cm")
        print(f"    Power peaking factor    = {np.max(self.power_normalized):.4f}")
        print(f"="*55 + "\n")
    
    def plot_flux(self, save_path=None):
        """Plot fast and thermal flux distribution."""
        fig, (ax1, ax2) = plt.subplots(2,1, figsize=(10,7), sharex = True)
        
        # Mark region boundaries
        # Find unique material transitions
        boundaries = self._find_boundaries()
        
        # Fast flux 
        ax1.plot(self.x, self.solver.phi1, 
                 color = '#e74c3c', linewidth = 2, label = 'Fast Flux Phi 1')
        ax1.set_ylabel("Fast flux (normalized)", fontsize = 12)
        ax1.set_title(f"PyReactor - 2-Group Neutron Flux | k-eff = {self.solver.k:.6f}",
                      fontsize = 13, fontweight = 'bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc = 'upper right')
        
        for b in boundaries:
            ax1.axvline(x=b, color='gray', linestyle = '--', alpha=0.7)
            
        # Thermal flux 
        ax2.plot(self.x, self.solver.phi2, 
                 color = '#2980b9', linewidth = 2, label = 'Thermal Flux Phi2')
        ax2.set_ylabel("Thermal flux (normalized)", fontsize = 12)
        ax2.set_xlabel("Position x (cm)", fontsize=12)
        ax2.set_title(f"PyReactor - 2-Group Neutron Flux | k-eff = {self.solver.k:.6f}",
                      fontsize = 13, fontweight = 'bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(loc = 'upper right')
        
        for b in boundaries:
            ax1.axvline(x=b, color='gray', linestyle = '--', alpha=0.7)
        
        self._add_region_labels(ax1, boundaries)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches = 'tight')
            print(f"    Flux plot saved: {save_path}")
        plt.show()
    
    def plot_power(self, save_path=None):
        """Plot normalized power distribution"""
        fig, ax = plt.subplots(figsize = (10,5))
        
        boundaries = self._find_boundaries()
        
        ax.plot(self.x, self.power_normalized, 
                color='#e67e22', linewidth = 2.5, label = 'Power Distribution')
        ax.fill_between(self.x, self.power_normalized, 
                        alpha=0.15, color = '#e67e22')
        
        # mark peak 
        peak_idx = np.argmax(self.power_normalized)
        ax.plot(self.x[peak_idx], self.power_normalized[peak_idx],
                'rv', markersize=12, label = f'Peak at x = {self.x[peak_idx]:.1f} cm')
        ax.axhline(y=1.0, color='red', linestyle=':', alpha=0.5)
        ax.set_xlabel("Position x (cm)", fontsize = 12)
        ax.set_ylabel("Normalized power", fontsize = 12)
        ax.set_title(f"PyReactor - Power Distribution | k-eff = {self.solver.k:.6f}", 
                     fontsize = 13, fontweight = 'bold')
        ax.grid(True, alpha =0.3)
        ax.legend(fontsize = 11)
        
        for b in boundaries:
            ax.axvline(x=b, color='gray', linestyle = '--', alpha=0.7)
        self._add_region_labels(ax, boundaries)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches = 'tight')
            print(f"    Power Plot saved: {save_path}")
        plt.show()
        
    def _find_boundaries(self):
        boundaries = []
        for regions in self.mesh.regions[1:]:
            boundaries.append(regions['start'])
        return boundaries
    
    def _add_region_labels(self, ax, boundaries):
        # Get y position for labels (top of plot)
        ymax = ax.get_ylim()[1]
        
        regions = self.mesh.regions
        for i, region in enumerate(regions):
            mid_x = (region['start'] + region['end'])/2
            ax.text(mid_x, ymax * 0.92, region['material'], 
                    ha = 'center', va = 'top', fontsize = 9,
                    color='gray', style = 'italic')