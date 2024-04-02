# YAML Reference
The config file is a YAML file defining:
* [Nodes](#nodes)
* [Connections](#connections)
* [Builders](#builders)
* [Pins](#pins)
* [Control](#control)

These sections can be defined in any order in the YAML file, but it is easiest to logically go through them in the order defined above.

There are sample config files in the `yaml` directory.

## Nodes
Nodes are the points that bars and strings connect at.

Nodes have a name and initial x, y, z positions.  
A node named `Node1` with x = 1, y = 2, and z = 0, it would look like:

```yaml
nodes:
    Node1: [1, 2, 0]
```


## Connections
Connections are how the nodes are connected to each other. There can be unlimited connection types, with each connection type having different properties as defined in the [Builders](#builders) section.

A connection type named `string` with a connection between `Node1` and `Node2` looks like:

```yaml
connections:
    string:
        - [Node1, Node2]
```

Connections can also optionally be named for later specifying connections to control.

```yaml
connections:
    string:
        - string1: [Node1, Node2] # Named connection
        - [Node2, Node3] # Unnamed connection
```

Connections whose builder has a `k` value and `pretension` (strings), can pass through multiple nodes. They are assumed to frictionlessly pass through nodes and therefore always have the same tension along it's entire length.

```yaml
connections:
    string:
        - string1: [Node1, Node2, Node5, Node6]
```

## Builders
Builders are the connection properties that define the strings or bars that hold the nodes together.
A builder must have a name matching a connection type in the `Connections` section.

For the `string` connection type with a stiffness (k) of 100N/m (it is actually unitless, but it helps me to think of everything in terms of metric units) and the string tensioned to 5N this section would look like:

```yaml
builders:
    string:
        stiffness: 100
        pretension: 5
```

If the tension is unknown but the unstretched length of the string is known, Hooke's Law can be used to calculate the initial tension: $F = k * (l_s - l)$ where $l_s$ is the stretched length of the string (distance between it's nodes) and $l$ is the unstretched length.

If a **connection type does not have a builder assigned to it, it is assumed to be a bar**, which is defined as a member able to transfer force along its length, while not changing in length.

## Pins
In 2D space the solved structure can float anywhere in the XY plane with any rotation unless we pin nodes (to define a place in XY space the structure is fixed to)

A pin needs a node name and a list of True/False values, with True indicating that the node is translationally pinned in that direction. To pin `Node1` in the x and y directions:
```yaml
pin:
  Node1: [True, True, False]
```

## Control
The `control` section defines which strings are able to be controlled (change length).

To define a control string the name of the connection, node the string is being pulled through, and the direction the string is being pulled need to be defined. For instance if the connection `String1` is being controlled, with extra length being pulled through `Node1` in the negative x direction:
```yaml
control:
  String1:
    node: Node1
    direction: [-1, 0, 0]
```

The magnitude of the direction vector doesn't matter for the solver, but does for the visualization, so if the arrow in the plot is larger than desired, the magnitude of the direction vector can be shrunk to the desired size.