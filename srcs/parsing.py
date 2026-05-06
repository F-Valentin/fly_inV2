class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, file_lines: list[str]) -> None:
        self._file_lines = file_lines
        self._zones: dict[str, Zone] = {}
        self._connections: list[Connection] = []

    def _get_nb_drones(self, line: str) -> int:
        try:
            nb_drones: int = int(line.split(":")[1])

            if nb_drones <= 0:
                raise ParsingError("nb_drones must be a positive integer.")

        except ValueError as e:
            raise e

        return nb_drones

    def _parse_zone(self, line: str) -> Zone:
        pass

    def _parse_connection(self, line: str) -> Connection:
        connection_data = line.split(":")[2].rstrip().split()

        zones_name = connection_data[0].split("-")

        if len(zones_name) == 1:
            pass

        try:
            start = self._zones[zones_name[0]]
            dest = self._zones[zones_name[1]]
        except KeyError as e:
            raise e
        
        if len(connection_data) == 2:
            pass

    def parse(self):
        data: dict[str, int | list[Zone] | list[Connection]] = {}
        next_line_index: int = 0

        for (i, line) in enumerate(self._file_lines):
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

        for line in self._file_lines[next_line_index:]:
            if not line.strip() or line.startswith("#"):
                continue

            if line.startswith("hub: "):
                pass
            elif line.startswith("connection: "):
                pass
            elif line.startswith("start_hub: "):
                pass
            elif line.startswith("end_hub: "):
                pass
            else:
                pass
