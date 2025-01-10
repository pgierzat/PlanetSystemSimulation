from classes.system import System
from pipr_24z_pgierzat.iomodule import load_config
import argparse
import sys


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to the configuration file")
    parser.parse_args(arguments)
    config = load_config(arguments[0])
    system = System(config)
    trajectories, collision_report = system.simulate(1)
    system.create_image(trajectories)
    system.save_collision_report(collision_report, "collision_report.txt")
    system.save_state("state.json")


if __name__ == "__main__":
    main(sys.argv[1:])
