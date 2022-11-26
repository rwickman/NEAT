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
        new_node = self.net.insert_node(link_rand, node_gid)

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

        # Add the links to the network
        self.net.add_link(link_in_hidden)
        self.net.add_link(link_hidden_out)

        # Increase the link count, for adding links/nodes between same nodes
        self.net.inc_link_count(link_rand)

        # Adjust the weights of the links
        link_in_hidden.trait.weight = 1.0 # Set 1.0 to make identity link
        link_in_hidden.trait.bias = 0.0 # Set 0.0 to have bias not affect anything
        link_hidden_out.trait.weight = link_rand.trait.weight # Set to mimic previous weight/bias
        link_hidden_out.trait.bias = link_rand.trait.bias

        return new_node


    def mutate_link_weights(self):
        """Randomly mutate the weights of the network."""
        for link in self.net.links:
            if random.uniform(0, 1) <= self.config.mutate_link_weight_rate:
                if random.uniform(0, 1) <= self.config.mutate_link_weight_rand_rate:
                    # Random init to new value
                    link.trait.init_trait()
                else:
                    # Randomly mutate link trait
                    link.trait.mutate()
    
    def mutate_add_link(self):
        """Randomly add a new link to the network."""

        # Conditions for adding a link:
        # 1. Link can't already exist
        # 2. Can't add link between output and output node
        # 3. Can't add link between input and input node
        # 4. Can't create cycle 

        cur_attempt = 0
        max_attempts = 20
        found = False
        while cur_attempt < max_attempts:
            cur_attempt += 1
            
            rand_depth = random.randint(0, len(self.net.depth_to_node) - 1)
            if rand_depth == len(self.net.depth_to_node) - 1:
                # Prevent connection between output nodes
                rand_in_depth = random.randint(0, len(self.net.depth_to_node) - 2)
                rand_out_depth = rand_depth

            elif rand_depth == 0:
                # Prevent connection between input nodes
                rand_out_depth = random.randint(1, len(self.net.depth_to_node)-1)
                rand_in_depth = rand_depth
            else:
                # Only allow for connection from a node in smaller depth to node in greater or equal depth
                rand_depth_2 = random.randint(0, len(self.net.depth_to_node)-1)
                if rand_depth >= rand_depth_2:
                    rand_out_depth = rand_depth
                    rand_in_depth = rand_depth_2
                else:
                    rand_out_depth = rand_depth_2
                    rand_in_depth = rand_depth

            # Choose random input and output nodes
            in_node = random.choice(self.net.depth_to_node[rand_in_depth])
            out_node = random.choice(self.net.depth_to_node[rand_out_depth])

            if self.net.get_link_count(in_node, out_node) > 0 or in_node.gid == out_node.gid:
                # Sanity-check, verify this method works correctly
                assert self.net.get_link_count(out_node, in_node) == 0
                continue
            else:
                found = True
                break
        
        # Sanity-check to verify got correct ordering
        assert out_node.depth >= in_node.depth

        # Check if a valid connection was found
        if found:
            # Create the new link
            created_link = Link(
                self.config,
                (in_node.gid, out_node.gid),
                in_node,
                out_node)

            # Simplest case, just add the connection as is
            if out_node.depth > in_node.depth:
                # Add link to network and outgoing node
                self.net.add_link(created_link)
            else:
                # This part requires shifting depth of output node
                #self.net.insert_dim(out_node.depth) # Shift all nodes up
                #in_node.depth = in_node.depth - 1 # Move it back down
                assert out_node.depth == in_node.depth
                self.net.move_node(out_node, out_node.depth, out_node.depth + 1)

                self.net.add_link(created_link)
                print(f"ADDED LINK {in_node.gid} --> {out_node.gid}")

            return created_link 