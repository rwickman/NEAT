import unittest

from neat.network import Network
from neat.node import Node
from neat.link import Link
from neat.trait import Trait
from neat.util import NodeType, ActivationType
from neat.mutator import Mutator
from neat.invocation_counter import InvocationCounter
from neat.reproduction import Reproduction
from test_util import *

class TestReproduce(unittest.TestCase):
    def test_mutate_nets_same(self):
        config = FooConfig()
        net_1 = setup_basic_network(config)
        inv_counter = InvocationCounter()
        inv_counter.gid_counter = 5
        mutator = Mutator(config, inv_counter)
        mutator.mutate_add_node(net_1)
        mutator.mutate_add_node(net_1)
        mutator.mutate_add_link(net_1)
        
        breeder = Reproduction(config)
        child_net = breeder.reproduce(net_1, net_1, 10.0, 0.0)
        self.assertEqual(len(child_net.links), len(net_1.links))

        for gid_tuple, link in net_1.links.items():
            child_link = child_net.links[gid_tuple]
            # Assert weights are equal
            self.assertEqual(child_link.trait.weight, link.trait.weight)
            self.assertEqual(child_link.trait.bias, link.trait.bias)

    # def test_mutate_nets_same_fitness(self):
    #     config = FooConfig()
    #     net_1 = setup_basic_network(config)
    #     inv_counter = InvocationCounter()
    #     inv_counter.gid_counter = 5
    #     mutator = Mutator(config, net_1, inv_counter)
    #     mutator.mutate_add_node()
    #     mutator.mutate_add_node()
    #     mutator.mutate_add_link()

    #     net_2 = setup_basic_network()
    #     breeder = Reproduction()
    #     child_net = breeder.reproduce(net_1, net_1, 0.0, 0.0)
    #     for gid_tuple in child_net.links.items():



        

if __name__ == '__main__':
    unittest.main()