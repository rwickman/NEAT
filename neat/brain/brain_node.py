import random

from neat.node import Node, OutNode
from neat.util import ActivationType, clamp, NodeType
from neat.brain.util import BrainNodeType

class BrainNode(Node):
    def __init__(self, args, gid, depth, node_type, activation_type=ActivationType.SIGMOID, brain_node_type=BrainNodeType.CHEMICAL):
        super().__init__(gid, depth, node_type, activation_type)
        self.args = args
        self.brain_node_type = brain_node_type
        self.is_refractory_period = False

    def copy(self):
        return ChemicalNode(self.args, self.gid, self.depth, self.node_type, self.activation_type)
    
    @property
    def activation(self):
        # This should only be called after setup_activation() or setting called
        assert self._activation is not None # sanity-check

        # If threshold has been reached, allow the full weight connection to be received
        if self.active_sum >= self.args.voltage_threshold:
            return 1
        else:
            return 0

    def _process(self):
        for link in self.incoming_links:
            # Only run through enabled links 
            if link.enabled:
                if isinstance(link.in_node, BrainNode) and link.in_node.brain_node_type == BrainNodeType.ELECTRICAL and link.in_node.activation == 1:
                    self.active_sum = self.args.voltage_threshold
                    break
                else:
                    if link.is_recur:
                        self.active_sum += link.trait.weight * link.in_node.prev_activation + link.trait.bias
                    else:
                        # Non-recurrent link
                        self.active_sum += link.trait.weight * link.in_node.activation + link.trait.bias


    def setup_activation(self):
        # Verify we are not trying to get output of sensor
        assert self.node_type != NodeType.SENSOR

        assert self._active_count == 0
        self._active_count += 1

        if self.args.use_refractory_period:
            if not self.is_refractory_period and self.active_sum >= self.args.voltage_rest:
                self._process()
        else:
            self._process()

        self._activation = 0

        self.active_sum = clamp(self.active_sum, self.args.voltage_min, self.args.voltage_threshold)
        if self.is_refractory_period and self.active_sum >= self.args.voltage_rest:
            self.is_refractory_period = False


    
    def _stabilize(self):
        # Add a random stabilizing value if the action potential has not been reached
        # if self.active_sum < self.args.voltage_threshold:
        voltage_diff = abs(self.active_sum - self.args.voltage_rest)
        rand_val = min(self.args.voltage_stabilize_magnitude, voltage_diff) 
        # rand_val = random.uniform(
        #     0, min(self.args.voltage_stabilize_magnitude, voltage_diff))
        if self.active_sum > self.args.voltage_rest:
            self.active_sum -= rand_val
        elif self.active_sum < self.args.voltage_rest:
            self.active_sum += rand_val
        

    def reset(self):
        if self.active_sum >= self.args.voltage_threshold:
            self.active_sum = self.args.voltage_min
            self.is_refractory_period = True

        self._prev_activation = self._activation if self._activation != None else 0 # Set to previous activation
        self._activation = None
        self._active_count = 0
        self._stabilize()
