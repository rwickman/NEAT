import argparse
from neat.environment.cart_pole import CartPole
from neat.environment.mountain_car import MountainCar
from neat.environment.lundar_lander import LundarLander
from neat.environment.lundar_lander_novelty import LundarLanderNovelty
from neat.environment.lundar_lander_brain import LundarLanderBrain

from neat.environment.cart_pole_brain import CartPoleBrain


def main(args):
    if args.env == "cartpole":
        env = CartPole(args)
    elif args.env == "lander":
        env = LundarLander(args)
    elif args.env == "lander_novelty":
        env = LundarLanderNovelty(args)
    elif args.env == "cartpole_brain":
        env = CartPoleBrain(args)
    elif args.env == "lander_brain":
        env = LundarLanderBrain(args)
    else:
        env = MountainCar(args)

    for i in range(100000):
        print(f"\nGeneration {i}")
        env.eval_population()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--init_weight_mean", type=float, default=0.0, 
        help="Mean of initial weight")
    parser.add_argument("--init_weight_std", type=float, default=0.4, 
        help="Std of initial weight")
    parser.add_argument("--weight_max", type=float, default=100.0, 
        help="Maximum value of weight.")
    parser.add_argument("--weight_min", type=float, default=-100.0, 
        help="Minimum value of weight.")
    
    parser.add_argument("--init_bias_mean", type=float, default=0.0, 
        help="Mean of initial bias")
    parser.add_argument("--init_bias_std", type=float, default=0.4, 
        help="Std of initial bias")
    parser.add_argument("--bias_max", type=float, default=100.0, 
        help="Maximum value of bias.")
    parser.add_argument("--bias_min", type=float, default=-100.0, 
        help="Minimum value of bias.")

    parser.add_argument("--mutate_link_weight_rate", type=float, default=0.8, 
        help="Probability of mutating all link weights.")
    parser.add_argument("--mutate_link_weight_rand_rate", type=float, default=0.05, 
        help="Likelihood of randomly initializing new link weight.")
    parser.add_argument("--mutate_weight_power", type=float, default=0.4, 
        help="Power of mutating a weight.")
    parser.add_argument("--mutate_add_node_rate", type=float, default=0.15, 
        help="Likelihood of randomly adding a new node.")
    parser.add_argument("--mutate_add_link_rate", type=float, default=0.30, 
        help="Likelihood of randomly adding a new link.")
    parser.add_argument("--mutate_enable_gene", type=float, default=0.25, 
        help="Likelihood of randomly enabling a gene.")
    parser.add_argument("--mutate_no_crossover", type=float, default=0.1, 
        help="Likelihood of copying a parent without crossover.")
    parser.add_argument("--mutate_add_recur_rate", type=float, default=0.0, 
        help="Likelihood of adding a recurrent link.")
    parser.add_argument("--reproduce_avg_trait_rate", type=float, default=0.5, 
        help="Likelihood of averaging the parents traits.")
    parser.add_argument("--reproduce_interspecies_rate", type=float, default=0.001, 
        help="Likelihood of reproducing across species.")


    parser.add_argument("--speciate_disjoint_factor", type=float, default=1.0, 
        help="Gene disjoint factor used for comparing two genotypes.")
    parser.add_argument("--speciate_weight_factor", type=float, default=3.0, 
        help="Gene trait weight factor used for comparing two genotypes.")
    parser.add_argument("--speciate_compat_threshold", type=float, default=3.0, 
        help="Gene trait weight factor used for comparing two genotypes.")
    parser.add_argument("--respeciate_size", type=int, default=2, 
        help="Size for respeciation.")
    parser.add_argument("--max_species", type=int, default=15, 
        help="Size for respeciation.")
    parser.add_argument("--init_species", type=int, default=15, 
        help="Number of initial species.")

    parser.add_argument("--init_pop_size", type=int, default=150, 
        help="Initial population size.")
    parser.add_argument("--survival_rate", type=float, default=0.2, 
        help="Percentage of organisms that will survive.")
    parser.add_argument("--env", default="cartpole", 
        help="Environment to run..")
    parser.add_argument("--max_stagnation", type=int, default=20,
        help="Maximum number of stagnation generations before the species is terminated.")
    parser.add_argument("--elites", type=int, default=2,
        help="Number of elites to preserve if a species is terminated.")

    parser.add_argument("--novelty_threshold", type=float, default=3.0,
        help="Threshold for avg distance in novelty to be added to novelty queue.")
    parser.add_argument("--novelty_queue_size", type=int, default=1000,
        help="Number of novelty final states in the queue.")
    parser.add_argument("--novelty_neighbors", type=int, default=15,
        help="Number of novelty neighbors used to compute novelty.")


    parser.add_argument("--voltage_min", type=float, default=-0.01,
        help="Minimum voltage of neuron.")
    parser.add_argument("--voltage_rest", type=float, default=0.0,
        help="Resting potential of neuron.")
    parser.add_argument("--voltage_threshold", type=float, default=0.03,
        help="Threshold needed to be reached for neuron to fire and action potential to occur.")
    parser.add_argument("--voltage_stabilize_magnitude", type=float, default=0.005,
        help="Random value added for stabilizing the voltage to its resting potential.")
    parser.add_argument("--electrical_node_rate", type=float, default=0.05,
        help="Probability of adding an electrical node.")
    parser.add_argument("--use_refractory_period", action="store_true",
        help="Use simulated period for neurons.")
    
    parser.add_argument("--use_brain", action="store_true",
        help="Use nodes modeled after the brain.")

    parser.add_argument("--save_file", default="models/population.json",
        help="Directory to save NEAT models.")
    parser.add_argument("--load", action="store_true",
        help="Load existing population from save_file.")
    
    

    args = parser.parse_args()
    main(args)