import math

from neat.node import OutNode
from neat.util import ActivationType, NodeType, clamp

class BrainOutputNode(OutNode):
    def __init__(self, gid, depth, node_type, activation_type=ActivationType.SIGMOID, out_pos=0):
        super().__init__(gid, depth, node_type, activation_type, out_pos)
    
    def copy(self):
        return BrainOutputNode(self.gid, self.depth, self.node_type, self.activation_type, self.out_pos)
    
    def setup_activation(self):
        # Verify we are not trying to get output of sensor
        assert self.node_type != NodeType.SENSOR

        assert self._active_count == 0
        self._active_count += 1
        
        for link in self.incoming_links:
            # Only run through enabled links 
            if link.enabled:
                if link.is_recur:
                    cur_act = int(link.in_node.prev_activation == 1)
                    self.active_sum += link.trait.weight * cur_act + link.trait.bias
                else:
                    cur_act = int(link.in_node.activation == 1)

                    # Non-recurrent link
                    self.active_sum += link.trait.weight * cur_act + link.trait.bias

        # Run through activation function
        if self.activation_type == ActivationType.SIGMOID:
            self._activation = 1 / (1 + math.exp(-clamp(self.active_sum, -100, 100)))
        else:
            self._activation = self.active_sum