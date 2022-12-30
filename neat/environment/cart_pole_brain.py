import gym
from neat.population import Population
from neat.nets.basic_nets import build_basic_brain_net
from neat.helpers.saving import save_population, load_population

class CartPoleBrain:
    def __init__(self, config, goal=3000):
        self.goal = goal
        self.config = config
        self.env = gym.make('CartPole-v1')
        # Create the population
        if self.config.load:
            # Load population
            self.population = load_population(config)
        else:
            self.population = Population(self.config)
            # Create the intitial population
            self.population.setup(
                build_basic_brain_net(self.config, 4, 1))

    def run(self, org, render=False):
        if render:
            self.env = gym.make('CartPole-v1', render_mode='human')
        else:
            self.env = gym.make('CartPole-v1')

        state, _ = self.env.reset()
        done = False
        total_reward = 0
        
        while not done:
            cur_actions = []
            for i in range(1):
                cur_actions.append(org(state)[0])
            out = sum(cur_actions) / len(cur_actions)
            
            action = 1 if out > 0.5 else 0

            state, reward, done, truncated, info = self.env.step(action)
            if render:
                self.env.render()     
            total_reward += reward
            if total_reward > self.goal:
                done = True

        
        org.net.reset()
        for node in org.net.nodes.values():
            node.active_sum = self.config.voltage_rest

        return total_reward

    def eval_population(self):
        max_fitness = 0
        best_org = None
        for org in self.population.orgs:
            org.update_fitness(self.run(org))
            if org.fitness > max_fitness:
                max_fitness = org.fitness
                best_org = org


        save_population(self.population, self.config.save_file)
        print("MAX FITNESS", max_fitness)
        if max_fitness > self.goal:
            print(best_org.net.nodes)

            self.run(best_org, True)

        self.population.evolve()


        
