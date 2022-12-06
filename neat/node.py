import math

from neat.util import NodeType, ActivationType

class Node:
    def __init__(self, gid, depth, node_type, activation_type=ActivationType.SIGMOID):
        # GID is global invocation number
        self.gid = gid

        # List of incoming Links
        self.incoming_links = []
        self.outgoing_links = [] # List of outgoing links

        self.active_sum = 0 # Current sum of all output actvations
        self._activation = None # Activation that corresponds to the output of a node
        self._prev_activation = 0 # Previous activation used for recurrent links

        self._depth = depth # Depth of this node in the network
        self.node_type = node_type # Type of node
        self.activation_type = activation_type
        self._active_count = 0

    def copy(self):
        return Node(self.gid, self.depth, self.node_type, self.activation_type)

    
    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, depth):
        self._depth = depth 
    
    
    @property
    def activation(self):
        # This should only be called after setup_activation() or setting called
        assert self._activation is not None # sanity-check
        
        return self._activation

    @property
    def prev_activation(self):
        # This should only be called after setup_activation() or setting called
        
        return self._prev_activation

    @activation.setter
    def activation(self, activation: float):
        """Manually set the activation. This should only be called for SENSORs or debugging/testing."""
        self._activation = activation
    
    def add_link(self, link):
        """Add link incoming into this node."""
        assert self.node_type != NodeType.SENSOR
        self.incoming_links.append(link)
    
    def add_outgoing_link(self, link):
        """Add links outgoing from this node."""
        assert (self.node_type == NodeType.OUT and link.is_recur) or self.node_type != NodeType.OUT
        self.outgoing_links.append(link)

    def setup_activation(self):
        # Verify we are not trying to get output of sensor
        assert self.node_type != NodeType.SENSOR

        assert self._active_count == 0
        self._active_count += 1
        
        for link in self.incoming_links:
            # Only run through enabled links 
            if link.enabled:
                if link.is_recur:
                    self.active_sum += link.trait.weight * link.in_node.prev_activation + link.trait.bias
                else:
                    # Non-recurrent link
                    self.active_sum += link.trait.weight * link.in_node.activation + link.trait.bias

        # Run through activation function
        if self.activation_type == ActivationType.SIGMOID:
            self.activation = 1 / (1 + math.exp(-self.active_sum))
        else:
            self.activation = self.active_sum


    def reset(self):
        """Reset the node. Should be called after network has been fully processed."""
        self.active_sum = 0
        self._prev_activation = self._activation if self._activation != None else 0 # Set to previous activation
        self._activation = None
        self._active_count = 0


class OutNode(Node):
    def __init__(self, gid, depth, node_type, activation_type=ActivationType.SIGMOID, out_pos=0):
        super().__init__(gid, depth, node_type, activation_type)
        self.out_pos = out_pos
    
    def copy(self):
        return OutNode(self.gid, self.depth, self.node_type, self.activation_type, self.out_pos)
