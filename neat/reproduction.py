import random

from neat.network import Network
from neat.node import Node, OutNode
from neat.util import NodeType

class Reproduction:
    def __init__(self):
        pass

    def reproduce(self, net_1, net_2, fitness_1, fitness_2):
        """Reproduce using two networks."""

        #child_net = Network(net_1.out_size)

        # Copy network from better node
        if fitness_1 > fitness_2:
            child_net = net_1.copy()
        elif fitness_1 < fitness_2:
            child_net = net_2.copy()
            net_1, net_2 = net_2, net_1 # Swap for easier transfering 
        else:
            # Randomly select a network to copy
            # TODO: In the future, do fine-tune mutation
            if random.random() >= 0.5:
                child_net = net_1.copy()
            else:
                child_net = net_2.copy()
                net_1, net_2 = net_2, net_1 # Swap for easier transfering 
        
        # Randomly select genes for shared genes
        for gid_tuple, link in net_1.links.items():
            if gid_tuple in net_2.links:
                # Choose a random gene to copy trait
                if random.random() >= 0.5:
                    # Already copied
                    pass
                else:
                    link_2 = net_2.links[gid_tuple]
                    child_net.links[gid_tuple].copy_trait(link_2)
                
        

        return child_net

                    
