import unittest

from neat.network import Network
from neat.node import Node
from neat.link import Link
from neat.trait import Trait
from neat.util import NodeType, ActivationType, detect_cycle, compute_depth
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
        self.assertEqual(len(net.depth_to_node[2]), 1)
        prev_gid = 5
        for i in range(100):
            new_node = mutator.mutate_add_node()
            self.assertEqual(new_node.gid, prev_gid + 1)
            prev_gid += 1
        
        # Assert correct number of nodes were added
        self.assertEqual(106, sum([len(net.depth_to_node[depth]) for depth in range(len(net.depth_to_node))]))
        self.assertEqual(106, len(net.nodes))
        self.assertEqual(len(net.hidden_nodes), 101)
        
        # Verify all the depths are correct
        for i in range(len(net.depth_to_node)):
            for j in range(len(net.depth_to_node[i])):
                self.assertEqual(compute_depth(net.depth_to_node[i][j], 0), i)
        
        
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
            for i in range(20):
                new_node = mutator.mutate_add_node()
                for d in range(len(net.depth_to_node)):
                    self.assertGreater(len(net.depth_to_node[d]), 0)
                mutator.mutate_add_link()

            
            # Verify all the depths are correct
            for i in range(len(net.depth_to_node)):
                for j in range(len(net.depth_to_node[i])):
                    self.assertEqual(net.depth_to_node[i][j].depth, i) 
                    self.assertEqual(compute_depth(net.depth_to_node[i][j], 0), i)
            
                
            # mutator.mutate_add_link()
            net.reset()
            net.activate([1,1])
    
    def test_mutate_link_weights(self):
        config = FooConfig()
        net = setup_basic_network(config)
        inv_counter = InvocationCounter()
        inv_counter.gid_counter = 5
        mutator = Mutator(config, net, inv_counter)
        mutator.mutate_link_weights()
    
    def test_detect_cycle(self):
        config = FooConfig()
        net = setup_basic_network(config)
        inv_counter = InvocationCounter()
        inv_counter.gid_counter = 5
        mutator = Mutator(config, net, inv_counter)

        new_node = mutator.mutate_add_node()

        self.assertTrue(detect_cycle(new_node, new_node.incoming_links[0].in_node))
        self.assertTrue(detect_cycle(new_node.outgoing_links[0].out_node, new_node.incoming_links[0].in_node))
        for i in range(2):
            for j in range(3):
                self.assertFalse(detect_cycle(net.nodes[i], net.end_nodes[j+2]))

    

if __name__ == '__main__':
    unittest.main()