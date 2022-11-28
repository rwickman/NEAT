import unittest

from neat.network import Network
from neat.node import Node
from neat.link import Link
from neat.trait import Trait
from neat.util import NodeType, ActivationType
from neat.mutator import Mutator
from neat.invocation_counter import InvocationCounter
from neat.population import Population
from test_util import *

class TestPopulatoin(unittest.TestCase):
    def test_speciate(self):
        config = FooConfig()
        net_1 = setup_basic_network(config)
        inv_counter = InvocationCounter()
        inv_counter.gid_counter = 5
        pop = Population(config)
        val = pop.speciate_fn(net_1, net_1)
        self.assertEqual(val, 0.0)

    def test_speciate_zero_weight(self):
        config = FooConfig()
        config.speciate_weight_factor = 0.0
        net_1 = setup_basic_network(config)
        inv_counter = InvocationCounter()
        inv_counter.gid_counter = 5
        net_2 = setup_basic_network(config)
        pop = Population(config)
        val = pop.speciate_fn(net_1, net_2)

        self.assertEqual(val, 0.0)
    
    def test_speciate_zero_weight_diff(self):
        config = FooConfig()
        config.speciate_weight_factor = 0.0
        net_1 = setup_basic_network(config)
        
        inv_counter = InvocationCounter()
        inv_counter.gid_counter = 5
        net_2 = setup_basic_network(config)
        mutator = Mutator(config, net_2, inv_counter)
        mutator.mutate_add_node()
        pop = Population(config)
        val = pop.speciate_fn(net_1, net_2)

        self.assertEqual(val, 2.0)
    

  
    def test_speciate_zero_weight_diff_two_mutate(self):
        config = FooConfig()
        config.speciate_weight_factor = 0.0
        net_1 = setup_basic_network(config)
        
        inv_counter = InvocationCounter()
        inv_counter.gid_counter = 5
        net_2 = setup_basic_network(config)
        mutator = Mutator(config, net_2, inv_counter)
        mutator.mutate_add_node()
        created_link = mutator.mutate_add_link()
        pop = Population(config)
        val = pop.speciate_fn(net_1, net_2)
        if created_link:
            self.assertEqual(val, 3.0)
        else:
            self.assertEqual(val, 2.0)

if __name__ == '__main__':
    unittest.main()