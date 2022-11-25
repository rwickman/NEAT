import math

from neat.util import NodeType, ActivationType
        
class Node:
    def __init__(self, gid, depth, node_type, activation_type):
        # GID is global invocation number
        self.gid = gid
        # self.units = []
        # List of incoming Links
        self.incoming_links = []
        self.active_sum = 0 # Current sum of all output actvations
        # self.active_count = 0 # M
        self._activation = None # Activation that corresponds to the output of a node
        self._depth = depth # Depth of this node in the network
        self.node_type = node_type # Type of node
        self.activation_type = activation_type

    
    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, depth):
        self._depth = depth 
    
    
    @property
    def activation(self):
        # This should only be called after setup_active_out()
        assert self._activation is not None # sanity-check
        
        return self._activation

    @activation.setter
    def activation(self, activation):
        """Manually set the activation. This should only be called for SENSORs or debugging/testing."""
        self._activation = activation
    
    def add_link(self, link):
        """Add link incoming into this node."""
        self.incoming_links.append(link)

    def setup_activation(self):
        # Verify we are not trying to get output of sensor
        assert self.node_type != NodeType.SENSOR

        for link in self.incoming_links:
            # Only run through enabled links 
            if link.enabled:
                self.active_sum += link.trait.weight * link.in_node.activation + link.trait.bias

        # Run through activation function
        if self.activation_type == ActivationType.SIGMOID:
            self.activation = 1 / (1 + math.exp(-self.active_sum))
        else:
            self.activation = self.active_sum


    def reset(self):
        """Reset the node. Should be called after network has been fully processed."""
        self.active_sum = 0
        self.activation = None