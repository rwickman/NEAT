import argparse
from neat.environment.cart_pole import CartPole
from neat.environment.mountain_car import MountainCar
from neat.environment.lundar_lander import LundarLander

def main(args):
    if args.env == "cartpole":
        env = CartPole(args)
    elif args.env == "lander":
        env = LundarLander(args)
    else:
        env = MountainCar(args)

    for i in range(100000):
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
    parser.add_argument("--mutate_link_weight_rand_rate", type=float, default=0.1, 
        help="Likelihood of randomly initializing new link weight.")
    parser.add_argument("--mutate_weight_power", type=float, default=0.4, 
        help="Power of mutating a weight.")
    parser.add_argument("--mutate_add_node_rate", type=float, default=0.15, 
        help="Likelihood of randomly adding a new node.")
    parser.add_argument("--mutate_add_link_rate", type=float, default=0.15, 
        help="Likelihood of randomly adding a new link.")
    parser.add_argument("--mutate_enable_gene", type=float, default=0.25, 
        help="Likelihood of randomly enabling a gene.")



    parser.add_argument("--speciate_disjoint_factor", type=float, default=1.0, 
        help="Gene disjoint factor used for comparing two genotypes.")
    parser.add_argument("--speciate_weight_factor", type=float, default=3.0, 
        help="Gene trait weight factor used for comparing two genotypes.")
    parser.add_argument("--speciate_compat_threshold", type=float, default=3.0, 
        help="Gene trait weight factor used for comparing two genotypes.")

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


    args = parser.parse_args()
    main(args)