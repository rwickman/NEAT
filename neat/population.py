

class Population:
    def __init__(self, config):
        self.config = config

    def speciate(self):
        pass

    def speciate_fn(self, net_1, net_2):
        """Compare two networks to determine if they should form a new species."""
        num_disjoint = 0
        num_shared = 0
        trait_diff = 0
        for link_gid in net_1.links:
            if link_gid not in net_2.links:
                num_disjoint += 1
            else:
                num_shared += 1
                trait_diff += net_1.links[link_gid].trait.distance(net_2.links[link_gid].trait)
                
        
        for link_gid in net_2.links:
            if link_gid not in net_1.links:
                num_disjoint += 1
        
        if num_shared == 0:
            num_shared = 1
        return self.config.speciate_disjoint_factor * num_disjoint + self.config.speciate_weight_factor * (trait_diff/num_shared)