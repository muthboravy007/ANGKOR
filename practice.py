# practice.py
# class exercise

# class Dog:
#     def __init__(self, name, breed, age):
#         self.name   = name 
#         self.breed  = breed
#         self.age    = age 
#         
#     def bark(self):
#         print(f"{self.name} says: Woof!")
#         
#     def is_puppy(self):
#         return self.age < 2
#     
# rex = Dog(name="Rex", breed="Labrador", age=3)
# 
# rex.bark()
# print(rex.is_puppy())

class Region:
    def __init__(self, name, x_min, x_max,
                 y_min, y_max, material):
        self.name       = name 
        self.x_min      = x_min 
        self.x_max      = x_max
        self.y_min      = y_min 
        self.y_max      = y_max 
        self.material   = material
    
    # We need to check if point (x,y) inside the rectangle?
    def contains(self,x,y):
        x_inside = self.x_min <= x <= self.x_max 
        y_inside = self.y_min <= y <= self.x_max 
        return x_inside and y_inside 
    
    # Print the summary 
    def describe(self):
        print(f"Region  : {self.name}")
        print(f"X range : {self.x_min} to {self.x_max}")
        print(f"Y range : {self.y_min} to {self.y_max}")
        print(f"Materials   : {self.material}")
        
# Test region---------------------
fuel = Region(
    name        = "fuel_center",
    x_min       = 20.0,
    x_max       = 80.0,
    y_min       = 20.0,
    y_max       = 80.0,
    material    = "uo2_fuel"
)

fuel.describe()

# Test contain() method 
print(fuel.contains(50,50))     # should be True 
print(fuel.contains(10,10))     # should be False
print(fuel.contains(20,20))     # should be Ture 

        