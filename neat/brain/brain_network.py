import random

from neat.network import Network
from neat.brain.chemical_node import ChemicalNode
from neat.brain.electrical_node import ElectricalNode
from neat.util import NodeType


class BrainNetwork(Network):
    def __init__(self, args, out_size=3, init_depth=2):
        super().__init__(out_size, init_depth)
        self.args = args
    
    def insert_node(self, link, node_gid):
        """When adding a node, you may need to shift the the depth of each node in path to end of network.""" 
        # if out_node.depth == in_node.depth + 1:
        #     self.insert_dim(out_node.depth) # Shift everything upward
        if random.random() <= self.args.electrical_node_rate:
            new_node = ElectricalNode(self.args, node_gid, link.in_node.depth + 1, NodeType.HIDDEN)
        else:
            new_node = ChemicalNode(self.args, node_gid, link.in_node.depth + 1, NodeType.HIDDEN)
        self.update_depth(new_node, link)
        # Sanity check, must not be equal as shift should have fixed this 
        assert new_node.depth != link.in_node.depth

        # Add the node to the network
        self.add_node(new_node)

        return new_node

    def copy(self):
        copy_net = BrainNetwork(self.args, self.out_size)
        # Copy the 
        copy_net.depth_to_node = [[] for _ in range(len(self.depth_to_node))]
        for gid_tuple, link in self.links.items():    
            # Get the input node
            if link.in_node.gid not in copy_net.nodes:
                # Create it if it doesn't exist
                in_node = link.in_node.copy()
                copy_net.add_node(in_node)
            else:
                in_node = copy_net.nodes[link.in_node.gid]

            # Get the output node
            if link.out_node.gid not in copy_net.nodes:
                # Create it if it doesn't exist
                out_node = link.out_node.copy()
                copy_net.add_node(out_node)
            else:
                out_node = copy_net.nodes[link.out_node.gid]

            assert gid_tuple == (in_node.gid, out_node.gid, link.is_recur)
            # Copy the link traits with a different in_node and out_node
            copy_link = link.copy(in_node, out_node)
            
            # Add the copied link to the copied network
            copy_net.add_link(copy_link)

            copy_net.link_dict[gid_tuple] = self.link_dict[gid_tuple]
            

        return copy_net