
class Organism:
    def __init__(self, config, net, gen=0, id=0):
        self.config = config
        self.net = net # The network controlling the behavior of the organism
        self.generation = gen # Tells what generation this organism is from
        self.fitness = 0
        self.best_fitness = -1000
        self.fitness_vals = []
        self.id = id

    def copy(self, id=0):
        copy_net = self.net.copy()
        return Organism(self.config, copy_net, self.generation, self.id)

    def update_fitness(self, fitness):
        self.fitness_vals.append(fitness)
        self.best_fitness = max(fitness, self.best_fitness)
        self.fitness = fitness

    @property
    def avg_fitness(self):
        if len(self.fitness_vals) == 0:
            return self.fitness

        return sum(self.fitness_vals) / len(self.fitness_vals) 

    def __call__(self, x):
        y = self.net.activate(x)
        self.net.reset()
        return y