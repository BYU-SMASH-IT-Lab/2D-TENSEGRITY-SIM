import matplotlib.pyplot as plt
import numpy as np

class Visualization:
    def __init__(self, Tensegrity, dim=2):
        """
        Initializes a Visualization object.

        Parameters:
        - Nodes (list): A list of Node objects representing the nodes in the tensegrity structure.
        - Connections (list): A list of Connection objects representing the connections between nodes.
        - dim (int): The dimension of the visualization (default is 2).
        """
        self.Nodes = Tensegrity.Nodes
        self.Connections = Tensegrity.Connections
        self.Pins = Tensegrity.Pins
        self.Controls = Tensegrity.Controls

        self.dim = dim

        self.fig, self.ax = plt.subplots()
    
    def plot(self, label_nodes: bool = False, label_connections: bool = False, label_forces: bool = False):
        """
        Plot the visualization of the tensegrity structure.

        Args:
            label_nodes (bool): Whether to label the node names in the plot. Default is False.
            label_connections (bool): Whether to label the connection names in the plot. Default is False.
            label_forces (bool): Whether to label the forces on the connections. Default is False.

        Raises:
            NotImplementedError: If the dimension is not 2.

        Returns:
            None
        """
        if self.dim == 2:
            self._plot_2d(label_nodes, label_connections, label_forces)
        else:
            raise NotImplementedError("3D visualization not implemented yet.")
        
    def _plot_2d(self, label_nodes: bool = False, label_connections: bool = False, label_forces: bool = False):
            """
            Plots the 2D visualization of the tensegrity structure.

            Parameters:
            - label_nodes (bool): If True, labels the nodes on the plot.

            Returns:
            - None
            """
            self.ax.clear()
            self.ax.set_aspect('equal')
            color_index = 1 # Using "CN" color cycle
            color_names = {}
            
            # --- Plot connections ---
            for connection in self.Connections:
                # Strings are dashed lines
                if connection.stiffness > 0:
                    # Set color
                    color = 'k'
                    if connection.name or len(connection.nodes) > 2:
                        color = f"C{color_index}"
                        if connection.name:
                            color_names[connection.name] = color_index
                        color_index += 1
                    
                    style = '--' if connection.force > 1e-3 else ':'
                    # Plot line
                    self.ax.plot([node.position[0] for node in connection.nodes], [node.position[1] for node in connection.nodes], f'{color}{style}')
                    
                
                # Bars are solid lines
                elif connection.stiffness == 0:
                    style = '-' if np.abs(connection.force) > 1e-3 else '-.'
                    self.ax.plot([connection.nodes[0].position[0], connection.nodes[1].position[0]], [connection.nodes[0].position[1], connection.nodes[1].position[1]], f'k{style}')

            # --- plot nodes and label ---
            for node in self.Nodes:
                # TODO: How to differentiate between 1D and 2D pinning?
                if node.name in self.Pins:
                    self.ax.plot(node.position[0], node.position[1], 'rX')
                else:
                    self.ax.plot(node.position[0], node.position[1], 'ko')
                if label_nodes:
                    self.ax.annotate(node.name, (node.position[0], node.position[1]), (.2, .2), textcoords='offset fontsize')
            
            if label_forces:
                for connection in self.Connections:
                    if connection.name:
                        self.ax.annotate(f"{connection.name}: {connection.force:.2f}", ((connection.nodes[0].position[0] + connection.nodes[1].position[0])/2, (connection.nodes[0].position[1] + connection.nodes[1].position[1])/2), ha='center')
                    else:
                        self.ax.annotate(f"{connection.force:.2f}", ((connection.nodes[0].position[0] + connection.nodes[1].position[0])/2, (connection.nodes[0].position[1] + connection.nodes[1].position[1])/2), ha='center')
            elif label_connections:
                for connection in self.Connections:
                    if connection.name:
                        self.ax.annotate(connection.name, ((connection.nodes[0].position[0] + connection.nodes[1].position[0])/2, (connection.nodes[0].position[1] + connection.nodes[1].position[1])/2), ha='center')

            # --- plot controls ---
            if self.Controls:
                for control in self.Controls:
                    color = f"C{color_names[control.connection.name]}" # Make sure the color matches the associated connection
                    self.ax.arrow(control.node.position[0], control.node.position[1], control.direction[0], control.direction[1], head_width=0.05, head_length=0.1, width=.01, color=color)

            self.fig.show()
