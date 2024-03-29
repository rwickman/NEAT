import math, os, random

from neat.invocation_counter import InvocationCounter
from neat.mutator import Mutator
from neat.species import Species
from neat.organism import Organism
from neat.reproduction import Reproduction
from neat.stagnation import Stagnation

class Population:
    """Maintains the population of organisms."""
    def __init__(self, args):
        self.args = args
        self.inv_counter = InvocationCounter()
        self.mutator = Mutator(self.args, self.inv_counter)
        self.breeder = Reproduction(self.args)
        self.cur_id = 1
        self.species_list = [] # List of different species
        self.stagnation = Stagnation(self.args)
        self.orgs = []
        self.generation = 0

    def setup(self, net):
        self.base_org = Organism(self.args, net)
        self.inv_counter.gid_counter = len(net.nodes)
        self.orgs = self.spawn(self.base_org, self.args.init_pop_size)
        self.speciate()

    def spawn(self, base_org, pop_size):
        """Spawn the initial population."""
        
        orgs = []
        
        for i in range(pop_size):
            copy_org = base_org.copy(self.cur_id) # Create a copy
            self.cur_id += 1
            prev_rand = self.args.mutate_link_weight_rand_rate
            self.args.mutate_link_weight_rand_rate = 1.0

            self.mutator.mutate_link_weights(copy_org.net) # Randomize the link weights
            self.args.mutate_link_weight_rand_rate = prev_rand
            orgs.append(copy_org) 
        
        return orgs

    def _create_species(self):
        """Create a new empty species."""
        species = Species(self.args, len(self.species_list))
        
        self.species_list.append(species)
        self.stagnation.add_species(species)

        return species

    def speciate(self):
        """Put the organisms into different species."""


        # # Create the first species
        # cur_species.add(self.orgs[0])
        
        # Put the rest of the organisms in a species
        cur_org_idx = 0
        for i in range(self.args.init_species):
            num_org = max(self.args.init_pop_size//self.args.init_species, 1)
            cur_species = self._create_species()
            print("num_org", num_org)
            for _ in range(num_org):
                cur_species.add(self.orgs[cur_org_idx])
                cur_org_idx += 1
        
        num_org_left = self.args.init_pop_size % self.args.init_species
        print("num_org_left", num_org_left)
        for i in range(num_org_left):
            self.species_list[i].add(self.orgs[cur_org_idx])
            cur_org_idx += 1
        
        
        # Put the rest of the organisms in a species
        assert cur_org_idx == len(self.orgs) 
                

    def respeciate(self):
        """Respeciate the population into different species that better match."""
        retained_orgs = set()
        # Keep few best orgs in each species 
        for species in self.species_list:
            species.orgs = species.orgs[:self.args.respeciate_size]
            for org in species.orgs:
                retained_orgs.add(org.id)

        # Find best matchgin species for each organism 
        for org in self.orgs:
            if org.id not in retained_orgs:
                random.shuffle(self.species_list)
                min_species_val = None
                best_species = None
                for i, cur_species in enumerate(self.species_list):
                    speciate_val = self.speciate_fn(org, cur_species.first())

                    if best_species == None or speciate_val < min_species_val:
                        min_species_val = speciate_val
                        best_species = cur_species

                # if min_species_val >= self.args.speciate_compat_threshold and len(self.species_list) < self.args.max_species:
                #     new_species = self._create_species()
                #     new_species.add(org)
                # else:
                #     best_species.add(org)
                best_species.add(org)


    def speciate_fn(self, org_1, org_2):
        """Compare two networks to determine if they should form a new species."""
        net_1 = org_1.net
        net_2 = org_2.net
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
        return self.args.speciate_disjoint_factor * num_disjoint + self.args.speciate_weight_factor * (trait_diff/num_shared)

    def prune_species(self, cur_species):
        # Randomize order so that sorting uniform avg fitness is random
        random.shuffle(cur_species.orgs)
        
        # Sort so best organisms are first
        cur_species.orgs.sort(key=lambda x: x.avg_fitness, reverse=True) 
        # Calculate how many organsims should remain "alive"
        num_live = int(math.ceil(max(self.args.survival_rate * len(cur_species.orgs), 2)))
        
        # Remove all but the top
        cur_species.orgs = cur_species.orgs[:num_live]


    def breed(self, cur_species):
        parent_1 = random.choice(cur_species.orgs)
        if random.random() <= self.args.mutate_no_crossover:
            parent_2 = parent_1
        else:
            if random.random() <= self.args.reproduce_interspecies_rate:
                # Choose a random organism across all the species
                parent_2 = random.choice(random.choice(self.species_list).orgs)
            else:
                parent_2 = random.choice(cur_species.orgs)

        child_net = self.breeder.reproduce(
            parent_1.net, parent_2.net, parent_1.avg_fitness, parent_2.avg_fitness)

        # Mutate the genotype
        self.mutate_child(child_net)
        

        new_org = Organism(
            self.args, child_net, gen=max(parent_1.generation, parent_2.generation) + 1, id=self.cur_id)

        # Increment the current organism ID
        self.cur_id += 1

        return new_org, parent_1, parent_2

    def _reset_species(self, cur_species, num_spawn):
        # The species has stagnated so remove them
        num_spawn = max(num_spawn, 2) - self.args.elites
        
        cur_species.orgs = cur_species.orgs[:self.args.elites]
        if num_spawn > 0:
            cur_species.orgs.extend(self.spawn(self.base_org, num_spawn)) 
        self.stagnation.reset(cur_species)
        print("RESETING", cur_species.species_id, "num_spawn", num_spawn)

    def evolve(self):
        self.generation += 1
        print("self.generation", self.generation)
        total_avg_fitness = 0
        min_fitness = min([cur_species.avg_fitness for cur_species in self.species_list])
        max_fitness = max([cur_species.avg_fitness for cur_species in self.species_list])
        print("max_fitness", max_fitness)
        print("min_fitness", min_fitness)
        if min_fitness == max_fitness:
            min_fitness -= 0.01

        for cur_species in self.species_list:
            cur_species.adj_fitness = (cur_species.avg_fitness - min_fitness) / (max_fitness - min_fitness)
            total_avg_fitness += cur_species.adj_fitness
        #print("EVOLVE LEN OF ORG SET: ", len(set([org.id for org in self.orgs])), "len(self.orgs)", len(self.orgs))
        self.orgs = []
        for cur_species in self.species_list:
            cur_species.age += 1 # Increase the age
            
            # Calculate how many new organisms to spawn
            if self.args.uniform_pop_distr:
                num_spawn = round((1/len(self.species_list)) * self.args.init_pop_size *  (1 - self.args.survival_rate))
            else:
                num_spawn = round((cur_species.adj_fitness / total_avg_fitness) * self.args.init_pop_size *  (1 - self.args.survival_rate))

            self.prune_species(cur_species)

            if self.stagnation.update(cur_species.species_id, cur_species.avg_fitness):
                self._reset_species(cur_species, num_spawn)
            else:
                # Spawn the new organisms
                new_orgs = []
                for _ in range(num_spawn):
                    new_org, _, _ = self.breed(cur_species)
                    new_orgs.append(new_org)

                for new_org in new_orgs:
                    cur_species.add(new_org)
                

            self.orgs.extend(cur_species.orgs)     
        
        if not self.args.no_respeciate:
            self.respeciate()
        assert len(set([org.id for org in self.orgs])) == len(self.orgs)
        print("len(self.orgs)", len(self.orgs))
          
    def mutate_child(self, child_net):
        if random.random() <= self.args.mutate_add_node_rate:
            self.mutator.mutate_add_node(child_net)
        
        if random.random() <= self.args.mutate_add_link_rate:
            self.mutator.mutate_add_link(child_net)
        
        if random.random() <= self.args.mutate_link_weight_rate:
            self.mutator.mutate_link_weights(child_net)

    def reset(self):
        """Reset all the organsisms in the population."""
        for org in self.orgs:
            org.reset()



        
            