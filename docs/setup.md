# Simulation Setup

The `main()` function in `2D-Tensegrity-Sim/main.py` can be changed to run the simulation as desired.

The primary parts to the simulations are:
* The parser
* The visualizer
* The optimizer

## Parser
This should be the first step to running the simulation. The takes the input yaml file from the commandline and creates the Tensegrity object.

```python
from yaml_parser import YamlParser

# Load the tensegrity system from the YAML file
tensegrity_system = YamlParser.parse(file)
```

## Visualizer
The `visualization` class takes in a `Tensegrity` object and can then be used to plot the tensegrity system using the `plot()` method.

```python
from visualization import Visualization as Viz

# Create the visualization object
viz = Viz(tensegrity_system)

viz.plot(label_nodes=True, label_connections=True)
```


