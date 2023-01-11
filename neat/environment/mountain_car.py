import gym
from neat.population import Population
from neat.nets.basic_nets import build_basic_net
from neat.util import ActivationType
from scipy.special import softmax

class MountainCar:
    def __init__(self, args, stop_point=-500, goal=-190):
        self.args = args
        self.stop_point = stop_point
        self.goal = goal
        self.env = gym.make('MountainCar-v0')
        self.population = Population(self.args)
        self.population.setup(
            build_basic_net(self.args, 2, 3, out_activation_type=ActivationType.IDENTITY))


    def run(self, org, render=False):
        if render:
            self.env = gym.make('MountainCar-v0', render_mode="human")
        else:
            self.env = gym.make('MountainCar-v0')
        state, _ = self.env.reset()
        done = False
        total_reward = 0

        while not done:
            action = softmax(org(state)).argmax()
            state, reward, done, truncated, info = self.env.step(action)
            total_reward += reward
            if total_reward <= self.stop_point:
                done = True
        
        total_reward = total_reward + 0.01# Make the total reward postive 
        return total_reward
    
    def eval_population(self):
        max_fitness = self.stop_point
        best_org = None
        for org in self.population.orgs:
            org.update_fitness(self.run(org))
            if org.fitness > max_fitness:
                max_fitness = org.fitness
                best_org = org
        
        
        print("MAX FITNESS", max_fitness)
        if max_fitness > self.goal:
            self.run(best_org, True)
            print("SHOWING BEST")
        
        

        self.population.evolve()