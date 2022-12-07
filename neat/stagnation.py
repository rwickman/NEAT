from dataclasses import dataclass

@dataclass
class SpeciesMetrics:
    last_update: int = 0
    best_avg_fitness: float = None

class Stagnation:
    """Detect stagnation in a species."""
    def __init__(self, config):
        self.config = config
        self.species_metrics: dict = {}

    def add_species(self, species):
        self.species_metrics[species.species_id] = SpeciesMetrics()

    def update(self, species_id, avg_fitness):
        if  self.species_metrics[species_id].best_avg_fitness == None or self.species_metrics[species_id].best_avg_fitness < avg_fitness:
            self.species_metrics[species_id].best_avg_fitness = avg_fitness
            self.species_metrics[species_id].last_update = 0
        else:
            self.species_metrics[species_id].last_update += 1

        return self.species_metrics[species_id].last_update >= self.config.max_stagnation

    def reset(self, species):
        self.species_metrics[species.species_id] = SpeciesMetrics()
        