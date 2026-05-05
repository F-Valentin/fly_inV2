class ParsingError(Exception):
    pass


def _get_nb_drones(line: str) -> int:
    try:
        nb_drones: int = int(line.split(":")[1])

        if nb_drones <= 0:
            raise ParsingError("nb_drones must be a positive integer.")

    except ValueError as e:
        raise e

    return nb_drones


def parse(file_lines: list[str]):
    data: dict[str, int | list[Zone] | list[Connection]] = {}

    for line in file_lines:
        if not line or line.startswith("#"):
            continue

        if line.startswith("nb_drones: "):
            try:
                nb_drones: int = _get_nb_drones(line)
            except (ValueError, ParsingError) as e:
                raise e

            data["nb_drones"] = nb_drones
            break

        raise ParsingError("The first line must contain nb_drones: X "
                           "(where X is a positive integer)")
