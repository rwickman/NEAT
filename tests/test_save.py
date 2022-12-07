import unittest

from neat.network import Network
from neat.helpers.saving import save_population, load_population
from neat.mutator import Mutator
from neat.invocation_counter import InvocationCounter
from neat.population import Population

from test_util import *
import random

class TestReproduce(unittest.TestCase):
    def test_save_and_load(self):
        config = FooConfig()
        net_1 = setup_basic_network(config)
        inv_counter = InvocationCounter()
        inv_counter.gid_counter = 5
        mutator = Mutator(config, inv_counter)
        
        # Add some random mutations
        mutator.mutate_add_node(net_1)
        mutator.mutate_add_node(net_1)
        mutator.mutate_add_node(net_1)
        mutator.mutate_add_link(net_1)
        mutator.mutate_link_weights(net_1)
        mutator.mutate_link_weights(net_1)

        # Create/setup the population
        population = Population(config)
        population.setup(net_1)
        for i in range(3):

            for org in population.orgs:
                # Assign random fitness value
                org.update_fitness(random.random())
            
            # Evolve the network
            population.evolve()
    
        for org in population.orgs:
                # Assign random fitness value
                org.update_fitness(random.random())
            
        
        # Save the population
        save_population(population, config.save_file)
        loaded_population = load_population(config)
        
        # Assert population level information is correct
        self.assertEqual(population.cur_id, loaded_population.cur_id)
        self.assertEqual(len(population.species_list), len(loaded_population.species_list))
        self.assertEqual(population.inv_counter.gid_counter, loaded_population.inv_counter.gid_counter)
        self.assertDictEqual(population.inv_counter.link_dict, loaded_population.inv_counter.link_dict)
        self.assertEqual(population.mutator.inv_counter.gid_counter, loaded_population.mutator.inv_counter.gid_counter)
        self.assertDictEqual(population.mutator.inv_counter.link_dict, loaded_population.mutator.inv_counter.link_dict)

        # Index the loaded organisms
        loaded_orgs = {}
        for org in loaded_population.orgs:
            loaded_orgs[org.id] = org
        
        # Iterate over all the organisms and check if they are equal
        for org  in population.orgs:
            loaded_org = loaded_orgs[org.id]

            # Assert that the organisms are equal
            self.assertEqual(loaded_org.id, org.id)
            self.assertEqual(loaded_org.generation, org.generation)
            self.assertEqual(loaded_org.best_fitness, org.best_fitness)
            self.assertEqual(loaded_org.avg_fitness, org.avg_fitness)


            # Index the loaded org depth_to_node list
            depth_to_node_dict = {}
            for depth, depth_list in enumerate(loaded_org.net.depth_to_node):
                depth_to_node_dict[depth] = set()
                for node in depth_list:
                    depth_to_node_dict[depth].add(node.gid)

            # Assert that their depth lists are equal
            for depth, depth_list in enumerate(org.net.depth_to_node):
                # Assert equal size
                self.assertEqual(len(depth_list), len(depth_to_node_dict[depth]))
                for node in depth_list:
                    # Assert the depth contains the correct nodes
                    self.assertIn(node.gid, depth_to_node_dict[depth])
            
            # Assert that their nodes are equal
            for gid, node in org.net.nodes.items():
                self.assertIn(gid, loaded_org.net.nodes)
                loaded_node = loaded_org.net.nodes[gid]

                # Assert the nodes values are the same
                self.assertEqual(node.gid, loaded_node.gid)
                self.assertEqual(node.depth, loaded_node.depth)
                self.assertEqual(len(node.incoming_links), len(loaded_node.incoming_links))
                self.assertEqual(len(node.outgoing_links), len(loaded_node.outgoing_links))
                self.assertEqual(node.node_type, loaded_node.node_type)
                self.assertEqual(node.activation_type, loaded_node.activation_type)
                
                for in_link in node.incoming_links:
                    found = False
                    found_link = None
                    for loaded_in_link in loaded_node.incoming_links:
                        if in_link.gid == loaded_in_link.gid:
                            found = True
                            found_link = loaded_in_link
                            break

                    self.assertTrue(found)
                    self.assertEqual(in_link.trait.weight, found_link.trait.weight)
                    self.assertEqual(in_link.trait.bias, found_link.trait.bias)
                    self.assertEqual(in_link.is_recur, found_link.is_recur)
                    self.assertEqual(in_link.enabled, found_link.enabled)
                
                for in_link in node.outgoing_links:
                    found = False
                    found_link = None
                    for loaded_out_link in loaded_node.outgoing_links:
                        if in_link.gid == loaded_out_link.gid:
                            found = True
                            found_link = loaded_out_link
                            break
                    self.assertTrue(found)
                    self.assertEqual(in_link.trait.weight, found_link.trait.weight)
                    self.assertEqual(in_link.trait.bias, found_link.trait.bias)
                    self.assertEqual(in_link.is_recur, found_link.is_recur)
                    self.assertEqual(in_link.enabled, found_link.enabled)
            
            # Assert their link count is equal
            self.assertDictEqual(org.net.link_dict, loaded_org.net.link_dict)

            # Check if all the links are equal
            self.assertEqual(len(org.net.links), len(loaded_org.net.links))
            for gid, link in org.net.links.items():
                # Verify the link is in the network
                self.assertIn(gid, loaded_org.net.links)
                loaded_net_link = loaded_org.net.links[gid]

                # Verify the link values are the same
                self.assertEqual(link.gid, loaded_net_link.gid)
                self.assertEqual(link.in_node.gid, loaded_net_link.in_node.gid)
                self.assertEqual(link.out_node.gid, loaded_net_link.out_node.gid)
                self.assertEqual(link.is_recur, loaded_net_link.is_recur)
                self.assertEqual(link.trait.weight, loaded_net_link.trait.weight)
                self.assertEqual(link.trait.bias, loaded_net_link.trait.bias)
    
        # Verify that the species are the same
        
        # First index the species from the loaded list
        species_dict = {}
        for species in loaded_population.species_list:
            # Verify no duplicate species
            self.assertNotIn(species.species_id, species_dict)
            species_dict[species.species_id] = species
        
        for species in population.species_list:
            # Verify species with the same ID is present
            self.assertIn(species.species_id, species_dict)
            loaded_species = species_dict[species.species_id]

            # Assert basic properties are equal
            self.assertEqual(len(loaded_species.orgs), len(species.orgs))
            self.assertEqual(loaded_species.age, species.age)
            self.assertEqual(loaded_species.species_id, species.species_id)
            
            org_set = set()
            for org in species.orgs:
                # Assert that no duplicate IDs have been added
                self.assertNotIn(org.id, org_set)
                org_set.add(org.id)
            
            loaded_org_set = set()
            for org in loaded_species.orgs:
                # Assert that no duplicate IDs have been added
                self.assertNotIn(org.id, loaded_org_set)
                loaded_org_set.add(org.id)
            
            self.assertSetEqual(org_set, loaded_org_set)
            






 




        
        
        

if __name__ == '__main__':
    unittest.main()