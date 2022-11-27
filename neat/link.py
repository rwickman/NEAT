
from neat.trait import Trait
from neat.node import Node

class Link:
    def __init__(self, config, in_node: Node, out_node: Node):
        # GID is (input node, output node)
        self.config = config
        self.gid = (in_node.gid, out_node.gid)
        self.trait = Trait(config)
        self.enabled = True
        self.in_node = in_node
        self.out_node = out_node

    def copy(self, in_node, out_node):
        copy_link = Link(self.config, in_node, out_node)
        copy_link.trait.weight = self.trait.weight
        copy_link.trait.bias = self.trait.bias
        return copy_link
    
    def copy_trait(self, other_link):
        self.trait.weight = other_link.trait.weight
        self.trait.bias = other_link.trait.bias