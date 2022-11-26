import random

from neat.network import Network
from neat.invocation_counter import InvocationCounter
from neat.link import Link
from neat.node import Node
from neat.util import NodeType


class Mutator:
    """Handles all mutation on a phenotype/network."""
    def __init__(self, config, net: Network, inv_counter: InvocationCounter):
        self.config = config
        self.net = net
        self.inv_counter = inv_counter

    def mutate_add_node(self):
        """Add a new node between a randomly selected link."""

        # Select a random link
        link_rand = random.choice(self.net.links)

        # Disable the selected link
        link_rand.enable = False

        # Retrive the GID
        node_gid = self.inv_counter.get_GID(
            link_rand.in_node.gid,
            link_rand.out_node.gid,
            self.net.get_link_count(link_rand.in_node, link_rand.out_node))
        
        # Create new node and optionally adjust depths of out_node
        new_node = self.net.insert_node(link_rand.in_node, link_rand.out_node, node_gid)


        # Create the links
        link_in_hidden = Link(
            self.config,
            (link_rand.in_node.gid, node_gid),
            link_rand.in_node,
            new_node)
        
        link_hidden_out = Link(
            self.config,
            (node_gid, link_rand.out_node.gid),
            new_node,
            link_rand.out_node)
        
        # Add the links to the nodes
        new_node.add_link(link_in_hidden)
        link_rand.out_node.add_link(link_hidden_out)

        # Add the links to the network
        self.net.add_link(link_in_hidden)
        self.net.add_link(link_hidden_out)

        # Adjust the weights of the links
        link_in_hidden.trait.weight = 1.0 # Set 1.0 to make identity link
        link_in_hidden.trait.bias = 0.0 # Set 0.0 to have bias not affect anything
        link_hidden_out.trait.weight = link_rand.trait.weight # Set to mimic previous weight/bias
        link_hidden_out.trait.bias = link_rand.trait.bias

        return new_node









