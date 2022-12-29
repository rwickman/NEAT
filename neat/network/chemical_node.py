from neat.node import Node

class ChemicalNode(Node):
    def __init__(self, gid, depth, node_type, activation_type=ActivationType.SIGMOID):
        