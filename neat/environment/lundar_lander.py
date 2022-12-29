import gym
from neat.population import Population
from neat.nets.basic_nets import build_basic_net
from neat.util import ActivationType
from scipy.special import softmax
import numpy as np
from neat.helpers.saving import save_population, load_population


class LundarLander:
    def __init__(self, config, stop_point=10000, goal=200, max_steps =1000):
        self.config = config
        self.stop_point = stop_point
        self.goal = goal
        self.max_steps = max_steps
        #self.reward_shift = reward_shift
        self.env = gym.make('LunarLander-v2')
        if config.load:
            self.population = load_population(config)
        else:
            self.population = Population(self.config)
            self.population.setup(
                build_basic_net(self.config, 8, 4, out_activation_type=ActivationType.IDENTITY))


    def run(self, org, render=False):
        if render:
            self.env = gym.make('LunarLander-v2', render_mode="human")
        else:
            self.env = gym.make('LunarLander-v2')
        state, _ = self.env.reset()
        done = truncated = False
        total_reward = 0
        steps = 0
        while not done and not truncated:
            out = org(state)
            
            action = np.random.choice(len(out), p=softmax(out))
            state, reward, done, truncated, info = self.env.step(action)
            
            total_reward += reward
            if total_reward >= self.stop_point:
                done = True
            steps += 1
            if steps > self.max_steps:
                done = True

        org.net.reset()
        return total_reward
    
    def eval_population(self):
        max_fitness = -1000
        best_org = None
        num_eval = 1
        for i in range(num_eval):
            for org in self.population.orgs:
                org.update_fitness(self.run(org))
                if i == num_eval - 1 and org.avg_fitness > max_fitness:
                    max_fitness = org.avg_fitness
                    best_org = org
        
        print("MAX FITNESS", max_fitness)
        # Save the population
        save_population(self.population, self.config.save_file)
        if max_fitness > self.goal:
            print("SHOWING BEST")
            print("SCORE", self.run(best_org, True))
            
        # Evolve the population
        self.population.evolve()