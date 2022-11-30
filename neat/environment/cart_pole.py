import gym
from neat.population import Population
from neat.nets.basic_nets import build_basic_net

class CartPole:
    def __init__(self, config, goal=2000):
        self.goal = goal
        self.config = config
        self.env = gym.make('CartPole-v1')
        # Create the population
        self.population = Population(self.config)
        # Create the intitial population
        self.population.setup(
            build_basic_net(self.config, 4, 1))

    def run(self, org, render=False):
        if render:
            self.env = gym.make('CartPole-v1', render_mode='human')
        else:
            self.env = gym.make('CartPole-v1')

        state, _ = self.env.reset()
        done = False
        total_reward = 0
        
        while not done:
            out = org(state)[0]
            action = 1 if out > 0.5 else 0

            state, reward, done, truncated, info = self.env.step(action)
            if render:
                self.env.render()     
            total_reward += reward
            if total_reward > self.goal:
                done = True

        return total_reward

    def eval_population(self):
        max_fitness = 0
        best_org = None
        for org in self.population.orgs:
            org.fitness = self.run(org)
            if org.fitness > max_fitness:
                max_fitness = org.fitness
                best_org = org
        

        print("MAX FITNESS", max_fitness)
        if max_fitness > self.goal:
            self.run(best_org, True)
        self.population.evolve()
