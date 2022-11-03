from simulation.simulate import simulate
from simulation.simulate_herman import simulate_herman
import argparse

# Next steps
# 2. Tuning with torch
# 4. Find better way of aggregating in numpy
# 4. Compare speed gains from parallelization
# 5. Compare speed gains from sparsification
# 7. Get torch_geometric on the cluster
# 8. Make network unaware of simulator

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n_neurons",    type=int,   default=20,                         help="Number of neurons in the network")
    parser.add_argument("-t", "--n_steps",      type=int,   default=10_000,                     help="Number of steps in simulation")
    parser.add_argument("-s", "--n_sims",       type=int,   default=1,                          help="Number of simulations to run")
    parser.add_argument("--data_path",          type=str,   default="data/simulation_data",     help="The path where the data should be saved")
    parser.add_argument("-p", "--max_parallel", type=int,   default=100,                        help="The max number of simulations to run in parallel")
    parser.add_argument("-f", "--firing_rate",  type=float, default=0.1,                        help="The average firing fate of the neurons")
    parser.add_argument("--herman",                                                             help="Run hermans simulation", action="store_true")
    args = parser.parse_args()

    print("Generating datasets...")
    print(f"Number of neurons:                            {args.n_neurons}")
    print(f"Number of simulations:                        {args.n_sims}")
    print(f"Number of steps:                              {args.n_steps}")
    print(f"Path to store data:                           {args.data_path}")
    print(f"Max number of simulation to run in parallel:  {args.max_parallel}")
    print(f"Average firing rate for the neurons:          {args.firing_rate}")

    if args.herman:
        simulate_herman(args.n_neurons, args.n_sims, args.n_steps, args.data_path, args.max_parallel, firing_rate=args.firing_rate)
    else:
        simulate(args.n_neurons, args.n_sims, args.n_steps, args.data_path, args.max_parallel, firing_rate=args.firing_rate)

if __name__ == "__main__":
    main()