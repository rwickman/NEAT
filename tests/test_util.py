from neat.network import Network
from neat.node import Node
from neat.link import Link
from neat.trait import Trait
from neat.util import NodeType, ActivationType


class FooConfig:
    def __init__(self):
        self.init_weight_mean = 0.0
        self.init_weight_std = 0.4
        self.weight_max = 100.0
        self.weight_min = -100.0
        
        self.init_bias_mean = 0.0
        self.init_bias_std = 0.4
        self.bias_max = 100.0
        self.bias_min = -100.0


def setup_basic_network(config, out_activation_type=ActivationType.SIGMOID):
    net = Network()

    """Create two sensor nodes"""
    sensor_node_1 = Node(0, 0, NodeType.SENSOR, ActivationType.IDENTITY)
    sensor_node_2 = Node(1, 0, NodeType.SENSOR, ActivationType.IDENTITY)
    
    # Add to network
    net.add_node(sensor_node_1, 0)
    net.add_node(sensor_node_2, 0)

    """Create three output nodes."""
    out_node_1 = Node(2, 1, NodeType.OUT, out_activation_type)
    out_node_2 = Node(3, 1, NodeType.OUT, out_activation_type)
    out_node_3 = Node(4, 1, NodeType.OUT, out_activation_type)

    # Add to network
    net.add_node(out_node_1, 1)
    net.add_node(out_node_2, 1)
    net.add_node(out_node_3, 1)

    # Add links between sensor and out nodes
    link_1_1 = Link(config, (0, 2), sensor_node_1, out_node_1)
    link_1_2 = Link(config, (0, 3), sensor_node_1, out_node_2)
    link_1_3 = Link(config, (0, 4), sensor_node_1, out_node_3)

    link_2_1 = Link(config, (1, 2), sensor_node_2, out_node_1)
    link_2_2 = Link(config, (1, 3), sensor_node_2, out_node_2)
    link_2_3 = Link(config, (1, 4), sensor_node_2, out_node_3)

    # Add links to nodes
    out_node_1.add_link(link_1_1)
    out_node_1.add_link(link_2_1)
    
    out_node_2.add_link(link_1_2)
    out_node_2.add_link(link_2_2)
    
    out_node_3.add_link(link_1_3)
    out_node_3.add_link(link_2_3)


    # Add links to network
    net.add_link(link_1_1)
    net.add_link(link_1_2)
    net.add_link(link_1_3)
    net.add_link(link_2_1)
    net.add_link(link_2_2)
    net.add_link(link_2_3)
    return net