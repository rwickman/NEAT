from neat.network import Network
from neat.node import Node, OutNode
from neat.link import Link
from neat.util import NodeType, ActivationType

from neat.brain.brain_network import BrainNetwork
from neat.brain.chemical_node import ChemicalNode
from neat.brain.brain_output_node import BrainOutputNode

def build_basic_net(args, num_sensor, num_output, out_activation_type=ActivationType.SIGMOID):
    """Create a basic fully connected network."""
    net = Network(num_output)
    sensor_nodes = []
    # Create the sensor nodes
    for i in range(num_sensor):
        sensor_node = Node(i, 0, NodeType.SENSOR, ActivationType.IDENTITY)
        sensor_nodes.append(sensor_node)

        net.add_node(sensor_node)
    
    # Create the output nodes
    for i in range(num_output):
        cur_id = i+num_sensor
        out_node = OutNode(cur_id, 1, NodeType.OUT, out_activation_type, out_pos=i)
        net.add_node(out_node)

        # Add links between sensor and out nodes
        for sensor_node in sensor_nodes:
            link = Link(args, sensor_node, out_node)
            net.add_link(link)

    return net

def build_basic_brain_net(args, num_sensor, num_output, out_activation_type=ActivationType.SIGMOID):
    """Create a basic fully connected network."""
    net = BrainNetwork(args, num_output, init_depth=3)
    sensor_nodes = []
    chemical_nodes = []
    # Create the sensor nodes
    for i in range(num_sensor):
        sensor_node = Node(i, 0, NodeType.SENSOR, ActivationType.IDENTITY)
        sensor_nodes.append(sensor_node)

        net.add_node(sensor_node)

    
    # Create the hidden chemical nodes
    for i in range(num_sensor):
        print("cur_id", i + num_sensor)
        chemical_node = ChemicalNode(args, i + num_sensor, 1, NodeType.HIDDEN)
        net.add_node(chemical_node)

        # Add links between sensor and out nodes
        for sensor_node in sensor_nodes:
            link = Link(args, sensor_node, chemical_node)
            net.add_link(link)

        chemical_nodes.append(chemical_node)

    # Create the output nodes
    for i in range(num_output):
        cur_id = i + (num_sensor * 2)
        print("cur_id", cur_id)
        out_node = BrainOutputNode(cur_id, 2, NodeType.OUT, out_activation_type, out_pos=i)
        net.add_node(out_node)

        # Add links between sensor and out nodes
        for chemical_node in chemical_nodes:
            link = Link(args, chemical_node, out_node)
            net.add_link(link)

    return net