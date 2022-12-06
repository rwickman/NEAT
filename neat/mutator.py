import random

from neat.network import Network
from neat.invocation_counter import InvocationCounter
from neat.link import Link
from neat.node import Node
from neat.util import NodeType, detect_cycle, compute_depth


class Mutator:
    """Handles all mutation on a phenotype/network."""
    def __init__(self, config, inv_counter: InvocationCounter):
        self.config = config
        self.inv_counter = inv_counter

    def mutate_add_node(self, net):
        """Add a new node between a randomly selected link."""

        # Select a random non-recurrent link
        non_recur_links = [link for link in list(net.links.values()) if not link.is_recur]
        link_rand = random.choice(non_recur_links)

        # Disable the selected link
        link_rand.enable = False

        # Retrive the GID
        node_gid = self.inv_counter.get_GID(
            link_rand.in_node.gid,
            link_rand.out_node.gid,
            net.get_link_count(link_rand.in_node, link_rand.out_node))
        
        # Create new node and optionally adjust depths of out_node
        new_node = net.insert_node(link_rand, node_gid)

        # Create the links
        link_in_hidden = Link(
            self.config,
            link_rand.in_node,
            new_node)
        
        link_hidden_out = Link(
            self.config,
            new_node,
            link_rand.out_node)

        # Add the links to the network
        net.add_link(link_in_hidden)
        net.add_link(link_hidden_out)

        # Increase the link count, for adding links/nodes between same nodes
        net.inc_link_count(link_rand)

        # Adjust the weights of the links
        link_in_hidden.trait.weight = 1.0 # Set 1.0 to make identity link
        link_in_hidden.trait.bias = 0.0 # Set 0.0 to have bias not affect anything
        link_hidden_out.trait.weight = link_rand.trait.weight # Set to mimic previous weight/bias
        link_hidden_out.trait.bias = link_rand.trait.bias

        return new_node

    def mutate_link_weights(self, net):
        """Randomly mutate the weights of the network."""
        for link in net.links.values():
            if random.random() <= self.config.mutate_link_weight_rate:
                if random.random() <= self.config.mutate_link_weight_rand_rate:
                    # Random init to new value
                    link.trait.init_trait()
                else:
                    # Randomly mutate link trait
                    link.trait.mutate()
    
    def mutate_add_link(self, net):
        """Randomly add a new link to the network."""

        # Conditions for adding a link:
        # 1. Link can't already exist
        # 2. Can't add link between output and output node
        # 3. Can't add link between input and input node
        # 4. Can't create cycle 

        cur_attempt = 0
        max_attempts = 30
        found = False

        if random.random() <= self.config.mutate_add_recur_rate:
            # Add a recurrent link
            created_link = self._create_recurrent_link(net)
            return created_link
        else:

            while cur_attempt < max_attempts:
                cur_attempt += 1
                
                rand_depth = random.randint(0, len(net.depth_to_node) - 1)
                if rand_depth == 0:
                    # Prevent connection between input nodes
                    rand_out_depth = random.randint(1, len(net.depth_to_node)-1)
                    rand_in_depth = rand_depth
                else:
                    rand_depth_2 = random.randint(0, len(net.depth_to_node)-1)
                    rand_out_depth = rand_depth
                    rand_in_depth = rand_depth_2

                # Choose random input and output nodes
                if len(net.depth_to_node[rand_in_depth]) == 0:
                    print("rand_in_depth", rand_in_depth)
                if len(net.depth_to_node[rand_out_depth]) == 0:
                    print("rand_out_depth", rand_out_depth)
                in_node = random.choice(net.depth_to_node[rand_in_depth])
                out_node = random.choice(net.depth_to_node[rand_out_depth])
                

                # Only add a link that doesn't exist, isn't recurrent, doesn't create a cycle, and in_node is not OUT node
                if ( net.get_link_count(in_node, out_node) > 0 or in_node.gid == out_node.gid or 
                    in_node.node_type == NodeType.OUT or detect_cycle(in_node, out_node)):
                    # Sanity-check, verify this method works correctly
                    # assert net.get_link_count(out_node, in_node) == 0
                    continue
                else:
                    found = True
                    break
            
            # # Sanity-check to verify got correct ordering
            # assert out_node.depth >= in_node.depth
            assert out_node.node_type != NodeType.SENSOR
            # Check if a valid connection was found
        

            if found:
                assert in_node.depth == rand_in_depth and out_node.depth == out_node.depth
                # Create the new link
                created_link = Link(
                    self.config,
                    in_node,
                    out_node)

                # Simplest case, just add the connection as is
                if out_node.depth > in_node.depth:
                    assert in_node.node_type != NodeType.OUT
                    # Add link to network and outgoing node
                    net.add_link(created_link)
                elif out_node.depth >= in_node.depth:
                    # Move the node to the -1 correct position
                    net.move_node(out_node, in_node.depth)
                    # This function will move the out_node and every outgoing node
                    net.update_depth(out_node, created_link)
                    net.add_link(created_link)



                return created_link 
    
    def _create_recurrent_link(self, net):
        
        cur_attempt = 0
        max_attempts = 30
        found = False
        net_nodes = list(net.nodes.values())
        while cur_attempt < max_attempts:
            in_node = random.choice(net_nodes)
            out_node = random.choice(net_nodes)
            
            if out_node.node_type == NodeType.SENSOR or net.get_link_count(in_node, out_node, is_recur=True) > 0:
                cur_attempt += 1
                continue

            found = True
            break
        
        if found:
            # Create the new link
            created_link = Link(
                self.config,
                in_node,
                out_node,
                is_recur=True)
            
            net.add_link(created_link)
        
            return created_link
