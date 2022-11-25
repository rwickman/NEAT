from neat.node import Node
from neat.link import Link
from neat.util import NodeType


class Network:
    def __init__(self):
        self.hidden_nodes: list[Node] = [] # List of hidden Nodes in the network
        self.end_nodes: list[Node] = [] # List of input/output Nodes in the network
        self.depth_to_node: list = [[] for i in range(2)] # Dictionary from depth to node
        self.links: list[Link] = [] # List of Links in the network
    
    def add_node(self, node, depth):
        # if depth not in self.depth_to_node:
        #     self.depth_to_node[depth] = []
        # TODO: How to handle depth -> node
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

        # Add the dimension at the depth
        self.depth_to_node[depth] = []


    def add_link(self, link):
        self.links.append(link)
    
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
                
                # Since last value, get final output
                if i == len(self.depth_to_node) - 1:
                    # sanity-check to verify only getting output from output node
                    assert node.node_type == NodeType.OUT 
                    outs.append(node.activation)
        
        return outs

    def reset(self):
        for i in range(len(self.depth_to_node)):
            for node in self.depth_to_node[i]:
                node.reset()

        
         

