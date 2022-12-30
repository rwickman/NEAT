from neat.brain.brain_node import BrainNode
from neat.util import ActivationType
from neat.brain.util import BrainNodeType

class ElectricalNode(BrainNode):
    def __init__(self, args, gid, depth, node_type, activation_type=ActivationType.SIGMOID, brain_node_type=BrainNodeType.ELECTRICAL):
        super().__init__(args, gid, depth, node_type, activation_type, brain_node_type)

    def copy(self):
        return ElectricalNode(self.args, self.gid, self.depth, self.node_type, self.activation_type)
    
    @property
    def activation(self):
        # This should only be called after setup_activation() or setting called
        assert self._activation is not None # sanity-check

        # If threshold has been reached, allow the full weight connection to be received
        if self.active_sum >= self.args.voltage_threshold:
            # Basically just cause the voltage it to trigger completely 
            return 1
        else:
            return 0