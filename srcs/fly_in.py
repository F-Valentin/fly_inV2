import sys

from typing import TYPE_CHECKING
from parsing import Parser, ParsingError
from solver import Solver
from drone import Drone
from path import Path
from simulation import Simulation, SimulationError

if TYPE_CHECKING:
    from zone import Zone


def main() -> None:
    """Read maps, parse input, solve paths, and run the drone simulation."""
    # args: list[str] = sys.argv

    # if len(args) != 2:
    #     print("The expected program argument is in the following format: "
    #           "python3 fly_in.py path_to_the_map.txt")
    #     sys.exit(1)

    # file_name: str = args[1]
    file_path = [
        # "maps/easy/01_linear_path.txt",
        # "maps/easy/02_simple_fork.txt",
        # "maps/easy/03_basic_capacity.txt",
        # "maps/medium/01_dead_end_trap.txt",
        # "maps/medium/02_circular_loop.txt",
        # "maps/medium/03_priority_puzzle.txt",
        # "maps/hard/01_maze_nightmare.txt",
        "maps/hard/02_capacity_hell.txt",
        # "maps/hard/03_ultimate_challenge.txt",
        # "maps/challenger/01_the_impossible_dream.txt",
    ]

    file_lines: list[str]
    for fp in file_path:
        print(fp)
        try:
            with open(fp) as f:
                file_lines = f.readlines()
        except (FileNotFoundError, PermissionError) as e:
            print(e)
            sys.exit(1)

        if not file_lines:
            print("The file is empty.")
            sys.exit(1)

        parser = Parser(file_lines)

        try:
            data = parser.parse()
        except (ParsingError, ValueError, KeyError) as e:
            print(e)
            sys.exit(1)

        start: Zone = data["start_hub"]
        end: Zone = data["end_hub"]

        all_paths = Solver.dfs(start, end)

        if not all_paths:
            print("No paths found")
            return

        drones = Drone.create_drones(data["nb_drones"])

        paths: list[Path] = []
        for path in all_paths:
            paths.append(Path(path))

        paths.sort(key=lambda p: (p.cost, -p.nb_of_priority_zones))

        Path.add_drones_to_paths(drones, paths)

        simulation = Simulation(end)

        try:
            turn = simulation.simulation(drones, paths)
        except SimulationError as e:
            print(e)
            sys.exit(1)
        print(f"turn: {turn}")


if __name__ == "__main__":
    main()
