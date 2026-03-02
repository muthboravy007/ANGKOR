
# Create Material class:
class Material:
    def __init__(self, name, D1, D2, sigma_a1, sigma_a2,
                 sigma_s12, nu_sigma_f1, nu_sigma_f2):
        self.name   = name 
        self.D1     = D1 
        self.D2     = D2
        self.sigma_a1 = sigma_a1
        self.sigma_a2 = sigma_a2
        self.sigma_s12 = sigma_s12
        self.nu_sigma_f1 = nu_sigma_f1
        self.nu_sigma_f2 = nu_sigma_f2 
    
    def __repr__(self):
        return (
            f"Material: {self.name}, "
            f"D1={self.D1}, D2={self.D2}, "
            f"sigma_a1={self.sigma_a1}, sigma_a2={self.sigma_a2}, "
            f"sigma_s12={self.sigma_s12}, "
            f"nu_sigma_f1={self.nu_sigma_f1}, "
            f"nu_sigma_f2={self.nu_sigma_f2}"
        )

class MaterialLibrary:
    def __init__(self):
        self.materials = {}
    
    def add_material(self, material):
        # storage material in self.materials
        # key = material.name, value = material object
        self.materials[material.name] = material 
        
    def get_material(self, name):
        # return the material if it exist
        # if not, raise an error with a clear message
        if name not in self.materials:
            raise KeyError(f"Material '{name}' not found in library!")
        return self.materials[name]
    
    def load_from_dict(self,data):
        # data look liks this from YAML:
        # { 
        #   "uo2_fuel": {"D1": 1.4, "D2:", 0.37, "sigma_a1": 0.0095,...},
        #   "water":    {"D1": 1.13,... }
        # }
        # Loop through and create Material objects:
        for name, props in data.items():
            mat = Material(
                name    = name, 
                D1      = props["D1"],
                D2      = props["D2"],
                sigma_a1= props["sigma_a1"],
                sigma_a2= props["sigma_a2"],
                sigma_s12 = props["sigma_s12"],
                nu_sigma_f1= props["nu_sigma_f1"],
                nu_sigma_f2= props["nu_sigma_f2"],
            )
            self.add_material(mat)

if __name__ == "__main__":
    uo2 = Material(
        name        = "uo2_fuel",
        D1          = 1.40,
        D2          = 0.37,
        sigma_a1    = 0.0095,
        sigma_a2    = 0.0820,
        sigma_s12   = 0.0210,
        nu_sigma_f1 = 0.0060,
        nu_sigma_f2 = 0.1350,
    )
    print(uo2)
    
    lib = MaterialLibrary()
    lib.add_material(uo2)
    
    retrieved = lib.get_material("uo2_fuel")
    print(f"Retrieved D2 = {retrieved.D2}")
    
    try: 
        lib.get_material("nonexistent")
    except KeyError as e:
        print(f"Error caught correctly: {e}")
    print("All tests passed!")