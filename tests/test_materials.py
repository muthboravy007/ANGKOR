# tests/test_materials.py

"""
    Unit tests for the materials module.
    Run with: pytest tests/test_materials.py -v 
"""

import pytest 
import sys, os 

sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..', 'pyreactor'))

from materials import Material, MaterialLibrary

class TestMaterial:
    ''' Tests for the material class'''
    def setup_method(self):
        self.uo2 = Material(
            name            = "uo2_fuel",
            D1              = 1.40,
            D2              = 0.37,
            sigma_a1        = 0.0095,
            sigma_a2        = 0.0820,
            sigma_s12       = 0.0210,
            nu_sigma_f1     = 0.0060,
            nu_sigma_f2     = 0.1350            
        )
    
    