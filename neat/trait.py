import random

from neat.util import clamp

class Trait:
    """Represents a weight and a bias for a connection."""
    def __init__(self, config):
        self.config = config
        self._init_weight()
        self._init_bias()
    

    def _init_weight(self):
        # Sample initial weight
        self.weight = random.gauss(
                self.config.init_weight_mean,
                self.config.init_weight_std)
        
        # Clamp the weight value
        self.weight = clamp(
            self.weight,
            self.config.weight_min,
            self.config.weight_max)
    
    def _init_bias(self):
        # Sample initial bias
        self.bias = random.gauss(
                self.config.init_bias_mean,
                self.config.init_bias_std)
        
        # Clamp the bias value
        self.bias = clamp(
            self.bias,
            self.config.bias_min,
            self.config.bias_max)
        
        