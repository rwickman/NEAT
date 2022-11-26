import argparse


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
    
    args = parser.parse_args()