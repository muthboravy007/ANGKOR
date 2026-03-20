import sys 

sys.path.insert(0, "angkor")
from input_reader import InputReader
from geometry_2d  import GeometryVisualizer

reader = InputReader("input/iaea_2d.yaml")
reader.read()

viz = GeometryVisualizer(reader.engine)
viz.plot_geometry(show_mesh=False, show_labels=False)