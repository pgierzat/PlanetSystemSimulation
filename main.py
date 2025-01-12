from classes.system import System
from iomodule import load_config
import argparse
import sys


def main(arguments):
    """
    Main function of the program.
    It parses the command line arguments, loads the configuration file
    Usage: python3 main.py -s [steps] -c [config_file]
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--steps", type=int,
        help="Number of steps to simulate",
        required=True
    )
    parser.add_argument(
        "-c", "--config", type=str,
        help="Path to the configuration file",
        required=True
    )
    parser.add_argument(
        "-o", "--output", type=str,
        help="Collision Report file", required=False,
        default="output.json"
    )
    parser.add_argument(
        "--state", type=str, help="State file", required=False,
        default="state.json"
    )
    args = parser.parse_args(arguments)
    config = load_config(args.config)
    system = System(config)
    trajectories, collision_report = system.simulate(args.steps)
    system.create_image(trajectories)
    system.save_collision_report(collision_report, args.output)
    system.save_state(args.state)


if __name__ == "__main__":
    main(sys.argv[1:])
