import unittest

from neat.network import Network
from neat.node import Node
from neat.link import Link
from neat.trait import Trait
from neat.util import NodeType, ActivationType
from test_util import *

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
        net.add_node(hidden_node)

        self.assertEqual(len(net.end_nodes), 5)
        self.assertEqual(len(net.hidden_nodes), 1)
        self.assertEqual(len(net.depth_to_node[0]), 2)
        self.assertEqual(len(net.depth_to_node[1]), 1)
        self.assertEqual(len(net.depth_to_node[2]), 3)


        # Disable link between last OUT node and first SENSOR node
        net.end_nodes[-1].incoming_links[0].enabled = False
        link_in_hidden = Link(config, net.end_nodes[0], hidden_node)
        link_hidden_out = Link(config, hidden_node, net.end_nodes[-1])
        
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
        net.add_node(hidden_node)

        self.assertEqual(len(net.end_nodes), 5)
        self.assertEqual(len(net.hidden_nodes), 1)
        self.assertEqual(len(net.depth_to_node[0]), 2)
        self.assertEqual(len(net.depth_to_node[1]), 1)
        self.assertEqual(len(net.depth_to_node[2]), 3)


        # Disable link between last OUT node and first SENSOR node
        net.end_nodes[-1].incoming_links[0].enabled = False
        self.assertEqual(net.end_nodes[-1].incoming_links[0].in_node.gid, net.end_nodes[0].gid)

        link_in_hidden = Link(config, net.end_nodes[0], hidden_node)
        link_hidden_out = Link(config, hidden_node, net.end_nodes[-1])

        link_in_hidden.trait.weight = 1.0 # Set weight to 1
        link_hidden_out.trait.weight = 1.0 # Set weight to 1

        # Add links to nodes
        # hidden_node.add_link(link_in_hidden)
        # net.end_nodes[-1].add_link(link_hidden_out)

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