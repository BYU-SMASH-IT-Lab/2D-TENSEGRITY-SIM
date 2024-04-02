from os.path import isfile
import yaml

from numpy import inf

from data_structures import Node, Connection, Control, Tensegrity

class YamlParser:
    """
    A class for parsing YAML files and creating a Tensegrity object.

    Attributes:
        None

    Methods:
        parse(file: str) -> Tensegrity:
            Parses the YAML file and returns a Tensegrity object.

    """

    @staticmethod
    def parse(file: str) -> Tensegrity:
        """
        Parses the YAML file and returns a tuple containing a list of nodes and a list of connections.

        Args:
            file (str): The path to the YAML file.

        Returns:
            Tensegrity: The tensegrity system containing Nodes and Connections.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        if not isfile(file):
            raise FileNotFoundError(f"The file {file} does not exist.")

        with open(file, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print("Invalid YAML file.")
                raise exc
            
            # TODO: make sure all floats are read in as floats, not strings (direction of [-.25, 0, 0] read in -.25 in as string)
            
            # --- Nodes ---
            Nodes = {} # Dictionary to store nodes so I can find them by name
            for node in data["nodes"]:
                Nodes[node] = (Node(node, data['nodes'][node]))


            # --- Connections ---
            Connections = [] # List to store connections used to create Tensegrity object
            connection_names = {} # Dictionary to store named connections
            
            for connection_type in data["connections"]:
                
                stiffness = 0 # Default stiffness
                pretension = 0 # Default pretension
                
                # --- Builders ---
                if connection_type in data["builders"]:
                    pretension = data["builders"][connection_type]["pretension"]
                    if data["builders"][connection_type]["stiffness"] == "inf": # TODO: how do we want to handle this? Needs to be implemented in solver if used
                        stiffness = inf
                    else:
                        stiffness = float(data["builders"][connection_type]["stiffness"])
                
                # Create connections
                for connection in data["connections"][connection_type]:
                    if type(connection) == dict: # If the connection has a name
                        for name, NodesList in connection.items():
                            connection = Connection([Nodes[n_name] for n_name in NodesList], connection_type, stiffness, pretension, name)
                            Connections.append(connection)
                            connection_names[name] = connection
                    else:
                        Connections.append(Connection([Nodes[n_name] for n_name in connection], connection_type, stiffness, pretension))
            

            # --- Pins ---
            Pins = {}
            if "pin" in data: # TODO: behavior, it is better to connect to the objects or should we just store the names?
                for pin in data["pin"]:
                    Pins[pin] = data["pin"][pin]

            # --- Control ---
            Controls = []
            if "control" in data: # TODO: behavior, it is better to connect to the objects or should we just store the names?
                for name in data["control"]:
                    node = Nodes[data["control"][name]["node"]] # Get node object
                    Controls.append(Control(connection_names[name], node, data["control"][name]["direction"]))

        return Tensegrity(list(Nodes.values()), Connections, Pins, Controls)
        