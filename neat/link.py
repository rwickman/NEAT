
from neat.trait import Trait
from neat.node import Node
import random

class Link:
    def __init__(self, args, in_node: Node, out_node: Node, is_recur: bool = False):
        # GID is (input node, output node)
        self.args = args
        self.gid = (in_node.gid, out_node.gid, is_recur)

        self.trait = Trait(args)
        self.enabled = True
        self.in_node = in_node
        self.out_node = out_node
        self.is_recur = is_recur # Indicates if the link is recurrent

    def copy(self, in_node, out_node):
        copy_link = Link(self.args, in_node, out_node, self.is_recur)
        copy_link.trait.weight = self.trait.weight
        copy_link.trait.bias = self.trait.bias
        copy_link.is_recur = self.is_recur
        return copy_link
    
    def copy_trait(self, other_link):
        self.trait.weight = other_link.trait.weight
        self.trait.bias = other_link.trait.bias
    
    def avg_traits(self, link_1, link_2):
        self.trait.weight = (link_1.trait.weight + link_2.trait.weight) / 2
        self.trait.bias = (link_1.trait.bias + link_2.trait.bias) / 2
    
    def dir_trait(self, link_1, link_2):
        self.trait.weight = link_1.trait.weight + random.gauss(0.0, self.args.mutate_weight_power) + random.gauss(0.0, self.args.mutate_weight_power) * (link_2.trait.weight - link_1.trait.weight)
        self.trait.bias = link_1.trait.bias + random.gauss(0.0, self.args.mutate_weight_power) + random.gauss(0.0, self.args.mutate_weight_power) * (link_2.trait.bias - link_1.trait.bias)



