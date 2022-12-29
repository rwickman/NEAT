import random

from neat.network import Network
from neat.node import Node, OutNode
from neat.util import NodeType

class Reproduction:
    def __init__(self, config):
        self.config = config

    def reproduce(self, net_1, net_2, fitness_1, fitness_2):
        """Reproduce using two networks."""

        #child_net = Network(net_1.out_size)
        avg_traits = random.random() <= self.config.reproduce_avg_trait_rate

        # Copy network from better node
        if fitness_1 > fitness_2:
            child_net = net_1.copy()
        elif fitness_1 < fitness_2:
            child_net = net_2.copy()
            net_1, net_2 = net_2, net_1 # Swap for easier transfering 
        else:
            # Randomly select a network to copy as fitness values are equal
            if random.random() >= 0.5:
                child_net = net_1.copy()
            else:
                child_net = net_2.copy()
                net_1, net_2 = net_2, net_1 # Swap for easier transfering 
        
        # Randomly select genes for shared genes
        for gid_tuple, link in net_1.links.items():
            if random.random() <= self.config.mutate_enable_gene:
                # Enable the gene if it was disabled    
                child_net.links[gid_tuple].enabled = True
            if gid_tuple in net_2.links:
                if avg_traits:
                    # Average the two parent traits
                    link_2 = net_2.links[gid_tuple]
                    child_net.links[gid_tuple].avg_traits(link, link_2)
                else:
                    # Choose a random gene to copy trait
                    if random.random() <= 0.5:
                        # Already copied
                        pass
                    else:
                        link_2 = net_2.links[gid_tuple]
                        child_net.links[gid_tuple].copy_trait(link_2)

                
        return child_net

    def reproduce_directional(self, net_1, net_2, fitness_1, fitness_2):
        # Copy network from better node
        if fitness_1 > fitness_2:
            child_net = net_1.copy()
        elif fitness_1 < fitness_2:
            child_net = net_2.copy()
            net_1, net_2 = net_2, net_1 # Swap for easier transfering 
        else:
            # Randomly select a network to copy as fitness values are equal
            if random.random() >= 0.5:
                child_net = net_1.copy()
            else:
                child_net = net_2.copy()
                net_1, net_2 = net_2, net_1 # Swap for easier transfering 
        
                    

        # Randomly select genes for shared genes
        for gid_tuple, link in net_1.links.items():
            if random.random() <= self.config.mutate_enable_gene:
                # Enable the gene if it was disabled    
                child_net.links[gid_tuple].enabled = True
            if gid_tuple in net_2.links:
                link_2 = net_2.links[gid_tuple]
                child_net.links[gid_tuple].dir_trait(link, link_2)

        return child_net