
class Organism:
    def __init__(self, config, net, gen=0, id=0):
        self.config = config
        self.net = net # The network controlling the behavior of the organism
        self.generation = gen # Tells what generation this organism is from
        self.fitness = 0
        self.best_fitness = -1000000
        self.id = id
        self._fitness_avg = 0
        self._num_updates = 0
        self.age = 0

    def copy(self, org_id=0):
        copy_net = self.net.copy()
        copy_org = Organism(self.config, copy_net, self.generation, org_id)
        copy_org.fitness = self.fitness
        copy_org.best_fitness = self.best_fitness
        copy_org._fitness_avg = self._fitness_avg
        copy_org._num_updates = self._num_updates
        copy_org.age = self.age
        copy_org.generation = self.generation
        return copy_org

    def update_fitness(self, fitness):
        self._num_updates += 1
        # Calculation the moving average
        self._fitness_avg += (fitness - self._fitness_avg) / self._num_updates
        self.best_fitness = max(fitness, self.best_fitness)
        self.fitness = fitness

    @property
    def avg_fitness(self):
        return self._fitness_avg 

    def reset(self):
        self.net.reset()

    def __call__(self, x):
        y = self.net.activate(x)
        self.net.reset()
        return y