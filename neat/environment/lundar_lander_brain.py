import gym
from neat.population import Population
from neat.nets.basic_nets import build_basic_net, build_basic_brain_net
from neat.util import ActivationType
from scipy.special import softmax
import numpy as np
from neat.brain.helpers.saving import save_population, load_population
from neat.brain.brain_reproduction import BrainReproduction

class LundarLanderBrain:
    def __init__(self, args, stop_point=10000, goal=200, max_steps=1000):
        self.args = args
        self.stop_point = stop_point
        self.goal = goal
        self.max_steps = max_steps
        #self.reward_shift = reward_shift
        self.env = gym.make('LunarLander-v2')
        if args.load:
            self.population = load_population(args)
        else:
            self.population = Population(self.args)
            self.population.setup(
                build_basic_brain_net(self.args, 8, 4, out_activation_type=ActivationType.IDENTITY))

        self.population.breeder = BrainReproduction(self.args)

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
            cur_outs = []
            # for i in range(3):
            #     out = org(state)
            #     cur_outs.append(out)

            #out = np.array(cur_outs).mean(0)
            out = org(state)
            action = np.random.choice(len(out), p=softmax(out))
            state, reward, done, truncated, info = self.env.step(action)
            
            total_reward += reward
            if total_reward >= self.stop_point:
                done = True
        
            steps += 1
        
            if steps > self.max_steps:
                done = True
        
        # for node in org.net.nodes.values():
        #     node.active_sum = self.args.voltage_rest
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
        save_population(self.population, self.args.save_file)
        print("SAVED")
        if max_fitness > self.goal:
            print(best_org.net.nodes)
            print("SHOWING BEST")
            print("SCORE", self.run(best_org, True))
            
        # Evolve the population
        self.population.evolve()