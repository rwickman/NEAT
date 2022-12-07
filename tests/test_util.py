from neat.network import Network
from neat.node import Node, OutNode
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

        self.mutate_link_weight_rate = 0.8
        self.mutate_link_weight_rand_rate = 0.1
        self.mutate_add_node_rate = 0.15
        self.mutate_add_link_rate = 0.30
        self.mutate_weight_power = 0.4
        self.mutate_enable_gene = 0.25
        self.mutate_no_crossover = 0.1
        self.mutate_add_recur_rate = 0.05
        self.reproduce_avg_trait_rate = 0.5

        self.speciate_disjoint_factor = 1.0
        self.speciate_weight_factor = 0.4
        self.speciate_compat_threshold = 15.0
        self.max_species = 10
        self.respeciate_size = 1

        self.save_file = "test_pop.json"

        self.init_pop_size = 150
        self.survival_rate = 0.2
        self.max_stagnation = 20
        self.elites = 2
        



def setup_basic_network(config, out_activation_type=ActivationType.SIGMOID):
    OUT_SIZE = 3
    net = Network(OUT_SIZE)

    """Create two sensor nodes"""
    sensor_node_1 = Node(0, 0, NodeType.SENSOR, ActivationType.IDENTITY)
    sensor_node_2 = Node(1, 0, NodeType.SENSOR, ActivationType.IDENTITY)
    
    # Add to network
    net.add_node(sensor_node_1)
    net.add_node(sensor_node_2)

    """Create three output nodes."""
    out_node_1 = OutNode(2, 1, NodeType.OUT, out_activation_type, out_pos=0)
    out_node_2 = OutNode(3, 1, NodeType.OUT, out_activation_type, out_pos=1)
    out_node_3 = OutNode(4, 1, NodeType.OUT, out_activation_type, out_pos=2)

    # Add to network
    net.add_node(out_node_1)
    net.add_node(out_node_2)
    net.add_node(out_node_3)

    # Add links between sensor and out nodes
    link_1_1 = Link(config, sensor_node_1, out_node_1)
    link_1_2 = Link(config, sensor_node_1, out_node_2)
    link_1_3 = Link(config, sensor_node_1, out_node_3)

    link_2_1 = Link(config, sensor_node_2, out_node_1)
    link_2_2 = Link(config, sensor_node_2, out_node_2)
    link_2_3 = Link(config, sensor_node_2, out_node_3)

    # Add links to nodes
    # out_node_1.add_link(link_1_1)
    # out_node_1.add_link(link_2_1)
    
    # out_node_2.add_link(link_1_2)
    # out_node_2.add_link(link_2_2)
    
    # out_node_3.add_link(link_1_3)
    # out_node_3.add_link(link_2_3)


    # Add links to network
    net.add_link(link_1_1)
    net.add_link(link_1_2)
    net.add_link(link_1_3)
    net.add_link(link_2_1)
    net.add_link(link_2_2)
    net.add_link(link_2_3)
    return net