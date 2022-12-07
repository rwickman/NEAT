
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

    def copy(self, id=0):
        copy_net = self.net.copy()
        return Organism(self.config, copy_net, self.generation, id)

    def update_fitness(self, fitness):
        self._num_updates += 1
        # Calculation the moving average
        self._fitness_avg += (fitness - self._fitness_avg) / self._num_updates
        self.best_fitness = max(fitness, self.best_fitness)
        self.fitness = fitness

    @property
    def avg_fitness(self):
        return self._fitness_avg 

    def __call__(self, x):
        y = self.net.activate(x)
        self.net.reset()
        return y