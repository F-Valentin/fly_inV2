class ParsingError(Exception):
    pass

class Parser:
    def __init__(self, file_lines: list[str]) -> None:
            self.file_lines = file_lines
            self.zones: dict[str, Zone] = {}
            self.connections: list[Connection] = []


    def _get_nb_drones(self, line: str) -> int:
        try:
            nb_drones: int = int(line.split(":")[1])

            if nb_drones <= 0:
                raise ParsingError("nb_drones must be a positive integer.")

        except ValueError as e:
            raise e

        return nb_drones


    def parse(self):
        data: dict[str, int | list[Zone] | list[Connection]] = {}
        next_line_index: int = 0

        for (i, line) in enumerate(self.file_lines):
            if not line.strip() or line.startswith("#"):
                continue

            if line.startswith("nb_drones: "):
                try:
                    nb_drones: int = self._get_nb_drones(line)
                except (ValueError, ParsingError) as e:
                    raise e

                data["nb_drones"] = nb_drones
                next_line_index = i + 1
                break

            raise ParsingError("The first line must contain nb_drones: X "
                            "(where X is a positive integer)")
        
        for line in self.file_lines[next_line_index:]:
            if not line.strip() or line.startswith("#"):
                continue