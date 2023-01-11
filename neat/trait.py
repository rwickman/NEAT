import random

from neat.util import clamp

class Trait:
    """Represents a weight and a bias for a connection."""
    def __init__(self, args):
        self.args = args
        self.init_trait()
        
    def init_trait(self):
        self._init_weight()
        self._init_bias()
    

    def _init_weight(self):
        # Sample initial weight
        self.weight = random.gauss(
                self.args.init_weight_mean,
                self.args.init_weight_std)
        
        # Clamp the weight value
        self.weight = clamp(
            self.weight,
            self.args.weight_min,
            self.args.weight_max)
    
    def _init_bias(self):
        # Sample initial bias
        self.bias = random.gauss(
                self.args.init_bias_mean,
                self.args.init_bias_std)
        
        # Clamp the bias value
        self.bias = clamp(
            self.bias,
            self.args.bias_min,
            self.args.bias_max)
        
    def mutate(self):
        self.weight = clamp(
            self.weight + random.gauss(0.0, self.args.mutate_weight_power),
            self.args.weight_min,
            self.args.weight_max)
        
        self.bias = clamp(
            self.bias + random.gauss(0.0, self.args.mutate_weight_power),
            self.args.bias_min,
            self.args.bias_max)
    
    
    def distance(self, other_trait):
        return abs(self.weight - other_trait.weight) + abs(self.bias - other_trait.bias)
