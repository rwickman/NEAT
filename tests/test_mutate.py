import unittest

from neat.network import Network
from neat.node import Node
from neat.link import Link
from neat.trait import Trait
from neat.util import NodeType, ActivationType
from neat.mutator import Mutator
from neat.invocation_counter import InvocationCounter
from test_util import *

class TestNetwork(unittest.TestCase):
    def test_mutate_add_node(self):
        config = FooConfig()
        net = setup_basic_network(config)
        inv_counter = InvocationCounter()
        inv_counter.gid_counter = 5

        mutator = Mutator(config, net, inv_counter)
        mutator.mutate_add_node()
        self.assertEqual(len(net.hidden_nodes), 1)
        self.assertEqual(len(net.depth_to_node), 3)
        self.assertEqual(len(net.depth_to_node[2]), 3)
        prev_gid = 5
        for i in range(100):
            new_node = mutator.mutate_add_node()
            self.assertEqual(new_node.gid, prev_gid + 1)
            prev_gid += 1
        
        # Assert correct number of nodes were added
        self.assertEqual(106, sum([len(net.depth_to_node[depth]) for depth in range(len(net.depth_to_node))]))

        self.assertEqual(len(net.hidden_nodes), 101)
        self.assertEqual(len(net.depth_to_node[-1]), 3)
        net.reset()
        print(net.activate([1,1]))
        # print(net.link_dict)

    def test_mutate_add_link(self):
        for i in range(100):
            config = FooConfig()
            net = setup_basic_network(config)
            inv_counter = InvocationCounter()
            inv_counter.gid_counter = 5
            mutator = Mutator(config, net, inv_counter)
            for i in range(10):
                new_node = mutator.mutate_add_node()

            # mutator.mutate_add_link()
            net.reset()
            print(net.activate([1,1]))

if __name__ == '__main__':
    unittest.main()