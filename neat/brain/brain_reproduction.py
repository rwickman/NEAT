from neat.reproduction import Reproduction


class BrainReproduction(Reproduction):
    def __init__(self, args):
        super().__init__(args)
    
    def reproduce(self, net_1, net_2, fitness_1, fitness_2):
        """Reproduce using two networks."""
        child_net = super().reproduce(net_1, net_2, fitness_1, fitness_2)

        # Set the active sum
        for gid, node in child_net.nodes.items():
            if gid in net_1.nodes and gid in net_2.nodes:
                node.active_sum = (net_1.nodes[gid].active_sum + net_2.nodes[gid].active_sum) / 2
            elif gid in net_1.nodes:
                node.active_sum = net_1.nodes[gid].active_sum
            elif gid in net_2.nodes:
                node.active_sum = net_2.nodes[gid].active_sum

        return child_net