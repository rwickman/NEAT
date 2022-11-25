import unittest

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

class TestNetwork(unittest.TestCase):
    def test_activate(self):
        config = FooConfig()
        net = setup_basic_network(config)

        self.assertEqual(len(net.links), 6)
        self.assertEqual(len(net.end_nodes), 5)
        print(net.activate([1, 1]))
    
    def test_one_hidden(self):
        config = FooConfig()
        net = setup_basic_network(config)

        # Create hidden node
        hidden_node = Node(10, 1, NodeType.HIDDEN, ActivationType.SIGMOID)
        net.insert_dim(1) # Shift all nodes over one
        net.add_node(hidden_node, 1)

        self.assertEqual(len(net.end_nodes), 5)
        self.assertEqual(len(net.hidden_nodes), 1)
        self.assertEqual(len(net.depth_to_node[0]), 2)
        self.assertEqual(len(net.depth_to_node[1]), 1)
        self.assertEqual(len(net.depth_to_node[2]), 3)


        # Disable link between last OUT node and first SENSOR node
        net.end_nodes[-1].incoming_links[0].enabled = False
        link_in_hidden = Link(config, (0, 10), net.end_nodes[0], hidden_node)
        link_hidden_out = Link(config, (10, 4), hidden_node, net.end_nodes[-1])
        
        net.add_link(link_in_hidden)
        net.add_link(link_hidden_out)

        # Create link
        print(net.activate([1, 1]))

    def test_one_hidden_all_zero_except_hidden(self):
        config = FooConfig()
        config.bias_max = 0.0
        config.bias_min = 0.0
        config.weight_max = 0.0
        config.weight_min = 0.0

        net = setup_basic_network(config, ActivationType.IDENTITY)

        # Create hidden node
        hidden_node = Node(10, 1, NodeType.HIDDEN, ActivationType.IDENTITY)
        net.insert_dim(1) # Shift all nodes over one
        net.add_node(hidden_node, 1)

        self.assertEqual(len(net.end_nodes), 5)
        self.assertEqual(len(net.hidden_nodes), 1)
        self.assertEqual(len(net.depth_to_node[0]), 2)
        self.assertEqual(len(net.depth_to_node[1]), 1)
        self.assertEqual(len(net.depth_to_node[2]), 3)


        # Disable link between last OUT node and first SENSOR node
        net.end_nodes[-1].incoming_links[0].enabled = False
        self.assertEqual(net.end_nodes[-1].incoming_links[0].in_node.gid, net.end_nodes[0].gid)

        link_in_hidden = Link(config, (0, 10), net.end_nodes[0], hidden_node)
        link_hidden_out = Link(config, (10, 4), hidden_node, net.end_nodes[-1])

        link_in_hidden.trait.weight = 1.0 # Set weight to 1
        link_hidden_out.trait.weight = 1.0 # Set weight to 1

        # Add links to nodes
        hidden_node.add_link(link_in_hidden)
        net.end_nodes[-1].add_link(link_hidden_out)

        net.add_link(link_in_hidden)
        net.add_link(link_hidden_out)

        # Create link
        self.assertListEqual([0.0, 0.0, 1.0], net.activate([1, 1]))
        net.reset()
        self.assertListEqual([0.0, 0.0, 2.0], net.activate([2, 3]))
        net.reset()
        self.assertListEqual([0.0, 0.0, 2.0], net.activate([2, 1]))
        net.reset()
        self.assertListEqual([0.0, 0.0, 5.0], net.activate([5, 100]))

if __name__ == '__main__':
    unittest.main()