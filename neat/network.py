from neat.node import Node
from neat.link import Link
from neat.util import NodeType

class Network:
    def __init__(self, out_size=3, init_depth=2, max_depth=-1):
        self.hidden_nodes: list[Node] = [] # List of hidden Nodes in the network
        self.end_nodes: list[Node] = [] # List of input/output Nodes in the network
        self.nodes: dict = {}
        self.max_depth = max_depth

        self.depth_to_node: list = [[] for i in range(init_depth)] # Dictionary from depth to node
        self.links: dict = {} # List of Links in the network
        self.link_dict: dict[tuple, int] = {} #map from link to number of links that have the same count
        self.out_size = out_size

    def add_node(self, node):
        depth = node.depth
        # if depth not in self.depth_to_node:
        #     self.depth_to_node[depth] = []
        self.depth_to_node[depth].append(node)

        assert node.gid not in self.nodes
        self.nodes[node.gid] = node

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

    def insert_node(self, link, node_gid):
        """When adding a node, you may need to shift the the depth of each node in path to end of network.""" 
        # if out_node.depth == in_node.depth + 1:
        #     self.insert_dim(out_node.depth) # Shift everything upward
        
        new_node = Node(node_gid, link.in_node.depth + 1, NodeType.HIDDEN)
        if self.max_depth != -1 and self.check_depth(new_node, link) - 1 >= self.max_depth:
            return None
        else:
            self.update_depth(new_node, link)
            # Sanity check, must not be equal as shift should have fixed this 
            assert new_node.depth != link.in_node.depth

            # Add the node to the network
            self.add_node(new_node)

            return new_node

    def move_node(self, node, new_depth):
        """Move a node to a different depth."""
        found = False
        for i, cur_node in enumerate(self.depth_to_node[node.depth]):
            if cur_node.gid == node.gid:
                self.depth_to_node[node.depth].pop(i)
                found = True
                break
        
        assert found
        if new_depth >= len(self.depth_to_node):
            self.depth_to_node.append([])

        self.depth_to_node[new_depth].append(node)
       
        node.depth = new_depth 

    def add_link(self, link):
        assert (link.in_node.gid, link.out_node.gid, link.is_recur) not in self.links
        self.links[(link.in_node.gid, link.out_node.gid, link.is_recur)] = link
        

        self.inc_link_count(link)
        
        # Add links to nodes
        link.in_node.add_outgoing_link(link)
        link.out_node.add_link(link)
        

    def inc_link_count(self, link):
        # Add to link counts 
        gid_tuple = (link.in_node.gid, link.out_node.gid, link.is_recur)
        if gid_tuple in self.link_dict:
            self.link_dict[gid_tuple] += 1
        else:
            self.link_dict[gid_tuple] = 1

    def get_link_count(self, in_node: Node, out_node: Node, is_recur: bool = False):
        if (in_node.gid, out_node.gid, is_recur) in self.link_dict:
            return self.link_dict[(in_node.gid, out_node.gid, is_recur)]        
        else:
            return 0

    def update_depth(self, node, link):
        cur_depth = node.depth + 1
        visit_links = [ link ]
        outgoing_links = []
        visited = set()
        while True:
            for cur_link in visit_links:
                if not cur_link.is_recur:
                    cur_node = cur_link.out_node
                    # if cur_node.gid in visited:
                    #     continue 
                    visited.add(cur_node.gid)

                    if cur_depth > cur_node.depth:
                        self.move_node(cur_node, cur_depth)

                        cur_node.depth = cur_depth
                        outgoing_links += cur_node.outgoing_links
                    
            cur_depth += 1
            
            if outgoing_links:
                visit_links = outgoing_links
                outgoing_links = []
            else:
                break

    def check_depth(self, node, link):
        cur_depth = node.depth + 1

        visit_links = [ link ]
        outgoing_links = []
        visited = set()
        while True:
            for cur_link in visit_links:
                if not cur_link.is_recur:
                    cur_node = cur_link.out_node
                    # if cur_node.gid in visited:
                    #     continue 
                    visited.add(cur_node.gid)

                    if cur_depth > cur_node.depth:
                        outgoing_links += cur_node.outgoing_links
                    
            cur_depth += 1
            
            if outgoing_links:
                visit_links = outgoing_links
                outgoing_links = []
            else:
                break
        print("cur_depth", cur_depth-1)
        return cur_depth

    def activate(self, x):
        """Run x through network."""

        # Run through sensor nodes
        for i, node in enumerate(self.depth_to_node[0]):
            node.activation = x[i]

        outs = [0 for _ in range(self.out_size)]

        # Iterate across all the depths
        for i in range(1, len(self.depth_to_node)):
            # Iterate across all the nodes in each depth
            for node in self.depth_to_node[i]:
                # Run input from each node to produce activation
                node.setup_activation()
                # print(f"DEPTH {i} ID {node.gid} NODE DEPTH {node.depth}")
                assert node.depth == i

                # Since last value, get final output
                if node.node_type == NodeType.OUT:
                    # sanity-check to verify only getting output from output node 
                    outs[node.out_pos] = node.activation
        
        return outs

    def reset(self):
        """Reset all the nodes."""
        for i in range(len(self.depth_to_node)):
            for node in self.depth_to_node[i]:
                node.reset()

    def copy(self):
        copy_net = Network(self.out_size)
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