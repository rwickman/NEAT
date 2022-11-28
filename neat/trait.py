import random

from neat.util import clamp

class Trait:
    """Represents a weight and a bias for a connection."""
    def __init__(self, config):
        self.config = config
        self.init_trait()
        
    def init_trait(self):
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
        
    def mutate(self):
        self.weight = clamp(
            self.weight + random.gauss(0.0, self.config.mutate_weight_power),
            self.config.weight_max,
            self.config.weight_min)
        
        self.bias = clamp(
            self.bias + random.gauss(0.0, self.config.mutate_weight_power),
            self.config.bias_max,
            self.config.bias_min)
    
    def distance(self, other_trait):
        return abs(self.weight - other_trait.weight) + abs(self.bias - other_trait.bias)
