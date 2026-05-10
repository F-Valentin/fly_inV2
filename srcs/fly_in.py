import sys

from parsing import Parser, ParsingError


def main() -> None:
    # args: list[str] = sys.argv

    # if len(args) != 2:
    #     print("The expected program argument is in the following format: "
    #           "python3 fly_in.py path_to_the_map.txt")
    #     sys.exit(1)

    # file_name: str = args[1]
    file_path = [
        "../maps/easy/01_linear_path.txt",
        # "../maps/easy/02_simple_fork.txt",
        # "../maps/easy/03_basic_capacity.txt",
        # "../maps/medium/01_dead_end_trap.txt",
        # "../maps/medium/02_circular_loop.txt",
        # "../maps/medium/03_priority_puzzle.txt",
        # "../maps/hard/01_maze_nightmare.txt",
        # "../maps/hard/02_capacity_hell.txt",
        # "../maps/hard/03_ultimate_challenge.txt",
        # "../maps/challenger/01_the_impossible_dream.txt",
    ]
    file_lines: list[str]
    for fp in file_path:
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
            parser.parse()
        except (ParsingError, ValueError, KeyError) as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    main()
