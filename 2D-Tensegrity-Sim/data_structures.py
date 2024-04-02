import numpy as np
from typing import List, Dict

class Node:
    """
    Represents a node in a 2D tensegrity structure.

    Attributes:
        name (str): The name of the node.
        position (numpy array(3,)): The position of the node in 3D space as a numpy array.
    """

    def __init__(self, name: str, position: list):
        if len(position) != 3:
            raise ValueError("Position input must contain exactly 3 numbers.")
        
        self.name = name
        self.position = np.array(position, dtype=float)

    def __str__(self):
        return f"Node: {self.name}  Position: {self.position}"
    
    def copy(self):
        return Node(self.name, self.position)

class Connection:
    """
    Represents a connection between nodes in a tensegrity structure.

    Attributes:
        type (str): The type of connection.
        nodes (List[Node]): The nodes involved in the connection.
    """

    def __init__(self, Nodes: List[Node], type: str, stiffness: float = 0, pretension: float = 0, name: str = None):
        self.nodes = Nodes

        # store original positions of nodes, for pinned connections.
        self.nodes_original = [node.copy() for node in Nodes]

        self.type = type # just stored for debugging purposes
        self.stiffness = stiffness
        self.force = pretension

        self.length = 0
        for i in range(len(self.nodes)-1):
            self.length += np.linalg.norm(self.nodes[i].position - self.nodes[i+1].position)
            
        if self.stiffness != 0:
            # Length is the distance between the nodes minus how much it is stretched
            # F = kx  ->  x = F/k
            self.length -= pretension/stiffness
        
        self.name = name
    
class Control:
    """
    Represents a control point in a tensegrity structure.

    Attributes:
        connection (Connection): The connection associated with the control point.
        node (Node): The node associated with the control point.
        direction (np.array): The direction the connection is pulled from the control point.

    """

    def __init__(self, connection: Connection, node: Node, direction: list):
        self.connection = connection
        self.node = node
        self.direction = np.array(direction, dtype=float)
    

class Tensegrity:
    def __init__(self, Nodes: List[Node], Connections: List[Connection], Pins: Dict[str, List[bool]] = [], Controls: List[Control] = []):
        self.Nodes = Nodes
        self.Connections = Connections
        self.Pins = Pins
        self.Controls = Controls
        self.ControlsDict = {control.connection.name: control for control in Controls} # TODO: use either this or the list, not both
    
    # TODO: Change method to use control strings instead of a named connections
    def change_connection_length(self, connection_name: str, delta: float):
        """
        Changes the length of a connection by a specified amount.

        Args:
            connection_name (str): The name of the connection to change.
            delta (float): The amount to change the length by.
        """
        for connection in self.Connections:
            if connection.name == connection_name:
                connection.length += delta
                return
        raise ValueError("Connection name not found.")
    