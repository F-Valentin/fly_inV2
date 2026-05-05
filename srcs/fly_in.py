import sys

from parsing import parse, ParsingError


def main() -> None:
    args: list[str] = sys.argv

    if len(args) != 2:
        print("The expected program argument is in the following format: "
              "python3 fly_in.py path_to_the_map.txt")
        sys.exit(1)

    file_name: str = args[1]
    file_lines: list[str]

    try:
        with open(file_name) as f:
            file_lines = f.readlines()
    except (FileNotFoundError, PermissionError) as e:
        print(e)
        sys.exit(1)

    if not file_lines:
        print("The file is empty.")
        sys.exit(1)
    try:
        parse(file_lines)
    except ParsingError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
