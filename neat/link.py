
from neat.trait import Trait
from neat.node import Node

class Link:
    def __init__(self, config, gid: tuple, in_node: Node, out_node: Node):
        # GID is (input node, output node)
        self.gid = gid
        self.trait = Trait(config)
        self.enabled = True
        self.in_node = in_node
        self.out_node = out_node

        #self.in_node.add_outgoing_link(self)
        #self.out_node.add_link(self)
