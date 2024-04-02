import argparse

from yaml_parser import YamlParser
from visualization import Visualization as Viz
from optimization import Optimizer

def main(file):
    # Load the tensegrity system from the YAML file
    tensegrity_system = YamlParser.parse(file)
    
    # Create the visualization object
    viz = Viz(tensegrity_system)


    # Plot the initial tensegrity system
    viz.plot(label_nodes=True, label_connections=True)

    # Solve the tensegrity system
    opt = Optimizer(tensegrity_system, d=2)
    opt.optimize()
    viz.plot(label_nodes=True, label_connections=True)

    d_length = get_float_input("Change connection length by (0 to exit): ")
    while d_length:
        tensegrity_system.change_connection_length("String1", d_length)
        opt.optimize()
        viz.plot(label_nodes=True, label_forces=True)
        d_length = get_float_input("Change connection length by (0 to exit): ")

    return

def get_float_input(prompt):
    while True:
        try:
            user_input = input(prompt)
            float_value = float(user_input)
            if float_value == 0:
                return None
            return float_value
        except ValueError:
            print("Invalid input. Please enter a valid floating-point number.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='2D Tensegrity Simulator')
    parser.add_argument("filename", help="YAML file to load", default="yaml/1-box.yaml")

    args = vars(parser.parse_args())
    main(file=args["filename"])