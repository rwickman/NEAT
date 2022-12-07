import math, os, random

from neat.invocation_counter import InvocationCounter
from neat.mutator import Mutator
from neat.species import Species
from neat.organism import Organism
from neat.reproduction import Reproduction
from neat.stagnation import Stagnation

class Population:
    """Maintains the population of organisms."""
    def __init__(self, config):
        self.config = config
        self.inv_counter = InvocationCounter()
        self.mutator = Mutator(self.config, self.inv_counter)
        self.breeder = Reproduction(self.config)
        self.cur_id = 1
        self.species_list = [] # List of different species
        self.stagnation = Stagnation(self.config)
        self.orgs = []

    def setup(self, net):
        self.base_org = Organism(self.config, net)
        self.inv_counter.gid_counter = len(net.nodes)
        self.orgs = self.spawn(self.base_org, self.config.init_pop_size)
        self.speciate()

    def spawn(self, base_org, pop_size):
        """Spawn the initial population."""
        
        orgs = []
        
        for i in range(pop_size):
            copy_org = base_org.copy(self.cur_id) # Create a copy
            self.cur_id += 1
            self.mutator.mutate_link_weights(copy_org.net) # Randomize the link weights
            orgs.append(copy_org) 
        
        return orgs

    def add_species(self, species):
        self.species_list.append(species)
        self.stagnation.add_species(species)

    def speciate(self):
        """Put the organisms into different species."""


        # # Create the first species
        # cur_species.add(self.orgs[0])
        
        # Put the rest of the organisms in a species
        cur_org_idx = 0
        for i in range(self.config.max_species):
            num_org = max(self.config.init_pop_size//self.config.max_species, 1)
            cur_species = Species(self.config, len(self.species_list))
            self.add_species(cur_species)
            for _ in range(num_org):
                cur_species.add(self.orgs[cur_org_idx])
                cur_org_idx += 1
                


        # for org in self.orgs:
        #     random.shuffle(self.species_list)
        #     found = False
        #     for cur_species in self.species_list:
        #         if self.speciate_fn(org.net, cur_species.first().net) < self.config.speciate_compat_threshold:
        #             cur_species.add(org)
        #             found = True
        #             break

        #     if not found:
        #         new_species = Species(self.config, len(self.species_list))
        #         new_species.add(org)
        #         self.add_species(new_species)
    
    def respeciate(self):
        """Respeciate the population into different species that better match."""
        retained_orgs = set()
        # Keep few best orgs in each species 
        for species in self.species_list:
            species.orgs = species.orgs[:self.config.respeciate_size]
            for org in species.orgs:
                retained_orgs.add(org.id)

        # Find best matchgin species for each organism 
        for org in self.orgs:
            if org.id not in retained_orgs:
                random.shuffle(self.species_list)
                min_species_val = None
                best_species = None
                for i, cur_species in enumerate(self.species_list):
                    speciate_val = self.speciate_fn(org.net, cur_species.first().net)

                    if best_species == None or speciate_val < min_species_val:
                        min_species_val = speciate_val
                        best_species = cur_species
                
                best_species.add(org)


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
    
    def evolve(self):
        total_avg_fitness = 0
        min_fitness = min([cur_species.avg_fitness for cur_species in self.species_list])
        max_fitness = max([cur_species.avg_fitness for cur_species in self.species_list])
        
        if min_fitness == max_fitness:
            min_fitness -= 0.01


        for cur_species in self.species_list:
            cur_species.adj_fitness = (cur_species.avg_fitness - min_fitness) / (max_fitness - min_fitness)
            total_avg_fitness += cur_species.adj_fitness
        #print("EVOLVE LEN OF ORG SET: ", len(set([org.id for org in self.orgs])), "len(self.orgs)", len(self.orgs))
        self.orgs = []
        for cur_species in self.species_list:
            cur_species.age += 1 # Increase the age
            num_spawn = math.ceil((cur_species.adj_fitness / total_avg_fitness) * self.config.init_pop_size *  (1 - self.config.survival_rate))
            cur_species.orgs.sort(key=lambda x: x.avg_fitness, reverse=True) # Sort so best organisms are first
            
            if self.stagnation.update(cur_species.species_id, cur_species.avg_fitness):
                # The species has stagnated so remove them
                num_spawn = max(num_spawn, 2) - self.config.elites
                
                cur_species.orgs = cur_species.orgs[:self.config.elites]
                if num_spawn > 0:
                    cur_species.orgs.extend(self.spawn(self.base_org, num_spawn)) 
                self.stagnation.reset(cur_species)
                print("RESETING", cur_species.species_id, "num_spawn", num_spawn)
            else:
                num_live = int(math.ceil(max(self.config.survival_rate * len(cur_species.orgs), 2)))
                cur_species.orgs = cur_species.orgs[:num_live] # Remove all but the top

                #print("num_spawn", num_spawn, "num_live", num_live)
                for _ in range(num_spawn):
                    parent_1 = random.choice(cur_species.orgs)
                    if random.random() <= self.config.mutate_no_crossover:
                        parent_2 = parent_1
                    else:
                        parent_2 = random.choice(cur_species.orgs)

                    child_net = self.breeder.reproduce(parent_1.net, parent_2.net, parent_1.fitness, parent_2.fitness)

                    self.mutate_child(child_net)
                    
                    # Mutate
                    cur_species.add(
                        Organism(self.config, child_net, gen=max(parent_1.generation, parent_2.generation) + 1, id=self.cur_id))

                    self.cur_id += 1

            self.orgs.extend(cur_species.orgs)     
            
        self.respeciate()
        assert len(set([org.id for org in self.orgs])) == len(self.orgs)
        print("len(self.orgs)", len(self.orgs))
          
    def mutate_child(self, child_net):
        if random.random() <= self.config.mutate_add_node_rate:
            self.mutator.mutate_add_node(child_net)
        
        if random.random() <= self.config.mutate_add_link_rate:
            self.mutator.mutate_add_link(child_net)
        
        if random.random() <= self.config.mutate_link_weight_rate:
            self.mutator.mutate_link_weights(child_net)


        







        
            