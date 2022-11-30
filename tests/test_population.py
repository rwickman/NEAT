import unittest

from neat.network import Network
from neat.node import Node
from neat.link import Link
from neat.trait import Trait
from neat.util import NodeType, ActivationType
from neat.mutator import Mutator
from neat.invocation_counter import InvocationCounter
from neat.population import Population
from neat.organism import Organism
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
        mutator = Mutator(config, inv_counter)
        mutator.mutate_add_node(net_2)
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
        mutator = Mutator(config, inv_counter)
        mutator.mutate_add_node(net_2)
        created_link = mutator.mutate_add_link(net_2)
        pop = Population(config)
        val = pop.speciate_fn(net_1, net_2)
        if created_link:
            self.assertEqual(val, 3.0)
        else:
            self.assertEqual(val, 2.0)

    def test_setup(self):
        config = FooConfig()
        net_1 = setup_basic_network(config)
        pop = Population(config)
        
        pop.setup(net_1)
        print("len(pop.species_list)", len(pop.species_list))
        for species in pop.species_list:
            print(len(species.orgs))


if __name__ == '__main__':
    unittest.main()