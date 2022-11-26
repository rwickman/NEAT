from neat.node import Node
from neat.link import Link
from neat.util import NodeType
class Network:
    def __init__(self):
        self.hidden_nodes: list[Node] = [] # List of hidden Nodes in the network
        self.end_nodes: list[Node] = [] # List of input/output Nodes in the network
        self.depth_to_node: list = [[] for i in range(2)] # Dictionary from depth to node
        self.links: list[Link] = [] # List of Links in the network
        self.link_dict: dict[tuple, int] = {} #map from link to number of links that have the same count


    def add_node(self, node, depth):
        # if depth not in self.depth_to_node:
        #     self.depth_to_node[depth] = []

        self.depth_to_node[depth].append(node)

        # Check if you need to add an end node or hidden node
        if depth == 0 or depth == len(self.depth_to_node) - 1:
            self.end_nodes.append(node)
        else:
            self.hidden_nodes.append(node)
    
    def insert_dim(self, depth):
        """Insert dimension by shifting all nodes at >= depth up one."""
        # Add an additional dimension
        self.depth_to_node.append([])

        # Iterate over all nodes at >= depth starting at the previous end
        for i in reversed(range(depth+1, len(self.depth_to_node))):
            # Shift up
            self.depth_to_node[i] = self.depth_to_node[i-1]
            for node in self.depth_to_node[i]:
                node.depth += 1

        # Add the dimension at the depth
        self.depth_to_node[depth] = []

    # def move_node(self, node, new_depth):
    #     """Move a node to a different depth."""
    #     if new_depth + 1 == len(self.depth_to_node):
    #         self.insert_dim(new_depth - 1)

    #     for i, cur_node in enumerate(self.depth_to_node[node.depth]):
    #         # Check if node is found
    #         if cur_node.gid == node.gid:
    #             # Remove the node from previous spot
    #             self.depth_to_node[node.depth].pop(i)
    #             # Move the node to the new spot
    #             self.depth_to_node[new_depth].append(node)
    #             node.depth = new_depth
    #             return


    def insert_node(self, in_node, out_node, node_gid):
        """When adding a node, you may need to shift the the depth of each node in path to end of network.""" 
        if out_node.depth == in_node.depth + 1:
            self.insert_dim(out_node.depth) # Shift everything upward
        
        new_node = Node(node_gid, out_node.depth - 1, NodeType.HIDDEN)

        # Sanity check, must not be equal as shift should have fixed this 
        assert new_node.depth != in_node.depth

        # Add the node to the network
        self.add_node(new_node, new_node.depth)

        return new_node

    def move_node(self, node, depth, old_depth):
        found = False
        for i, cur_node in enumerate(self.depth_to_node[old_depth]):
            if cur_node.gid == node.gid:
                self.depth_to_node[old_depth].pop(i)
                found = True
                break
        
        assert found
       
        self.depth_to_node[depth].append(node)
       
        node.depth = depth 

    def add_link(self, link):
        self.links.append(link)
        self.inc_link_count(link)

    def inc_link_count(self, link):
        # Add to link counts 
        gid_tuple = (link.in_node.gid, link.out_node.gid)
        if gid_tuple in self.link_dict:
            self.link_dict[gid_tuple] += 1
        else:
            self.link_dict[gid_tuple] = 1

    def get_link_count(self, in_node: Node, out_node: Node):
        if (in_node.gid, out_node.gid) in self.link_dict:
            return self.link_dict[(in_node.gid, out_node.gid)]        
        else:
            return 0

    # def fix_depth(self):
    #     """Fix the depth of all the nodes."""
    #     out_nodes = [node for node in self.end_nodes if node.node_type == NodeType.OUT]
    #     gid_to_depth = {}
    #     def traverse(cur_node, depth):
    #         for cur_node.incoming_links


    def activate(self, x):
        """Run x through network."""

        # Run through sensor nodes
        for i, node in enumerate(self.depth_to_node[0]):
            node.activation = x[i]

        outs = []
        # Iterate across all the depths
        for i in range(1, len(self.depth_to_node)):
            # Iterate across all the nodes in each depth
            for node in self.depth_to_node[i]:
                # Run input from each node to produce activation
                node.setup_activation()
                # print(f"DEPTH {i} ID {node.gid} NODE DEPTH {node.depth}")
                assert node.depth == i

                # Since last value, get final output
                if i == len(self.depth_to_node) - 1:
                    # sanity-check to verify only getting output from output node
                    assert node.node_type == NodeType.OUT 
                    outs.append(node.activation)
        
        return outs

    def reset(self):
        """Reset all the nodes."""
        for i in range(len(self.depth_to_node)):
            for node in self.depth_to_node[i]:
                node.reset()

    # def mutate_add_node(self):
    #     """Add a mutation for adding nodes."""
    #     # Select a random link to add a node between
        
         

