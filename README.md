# 2D Tensegrity Sim

## About
This repo contains code to create a simulation for 2D Tensegrity structures specifically tailored to the needs of the Elbow Brace Project.

## Getting started
I reccommend using a venv to keep the libraries for this project separate from the main python interpreter. To create a venv, from the project's main directory run `python3 -m venv ./venv`. Now everytime you want to use this venv run `source venv/bin/activate`. To deactivate simply use the `deactivate` command. 

This project uses Python3, in order to run it you will need some dependencies. To get them you can run `pip install -r requirements.txt` (with the venv active)

To run the project:
```bash
python3 2D-Tensegrity-Sim/main.py <path/to/yaml/config>
```
Sample yaml config files are provided in the `yaml` directory. To understand how to change the simulation to your needs, see the [simulation setup](docs/setup.md) documentation. 

## Definitions and Conventions (as used in this project)
Strings - Strings are connection types that only carry tension, they lengthen as force is applied  
Bar - A bar can carry either tension or compression, but does not change length  
Forces - Tensions are positive values and compression forces in connections are negative.


## Organization
### 2D-Tensegrity-Sim
The `2D-Tensegrity-Sim` directory contains all the code for the project.
* `main.py` is the primary file to run the project. It take as an input a yaml file
* `data_structures.py` contains the `Node`, `Connection`, `Control`, and `Tensegrity` classes
* `yaml_parser.py` reads the yaml file and returns the Tensegrity object. See [YAML Doc](docs/yaml.md) for how to format the yaml file
* `visualization.py` shows the tensegrity structure using matplotlib
* `optimization.py` uses an optimizer to solve for an updated structure (through the `Tensegrity.change_connection_length()` function)

### yaml
The `yaml` directory contains sample yaml files for running the sim

# Ideas for future implementation
* Create GUI to help create yaml files
    * yaml file contains just nodes and gui has interface to define how they are connected
    * Allow easy "tiling" of single cells to n x m cells
* Add error checking on Yaml file while parsing
    * No unused nodes
    * builder name matches a connection name
    * connections use valid node names