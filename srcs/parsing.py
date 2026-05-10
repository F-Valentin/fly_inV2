from connection import Connection
from zone import Zone, ZoneMetadata


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, file_lines: list[str]) -> None:
        self._file_lines = file_lines
        self._zones: dict[str, Zone] = {}
        self._connections: list[Connection] = []
        self._current_line: int = 0

    def _get_nb_drones(self, line: str) -> int:
        try:
            nb_drones: int = int(line.split(":")[1])

            if nb_drones <= 0:
                raise ParsingError("nb_drones must be a positive integer.")

        except ValueError as e:
            raise ValueError(f"nb_drones value missing, got: {e}")

        return nb_drones

    def _parse_zone_metadata(self, line: str) -> ZoneMetadata:
        zone_metadata: ZoneMetadata = ZoneMetadata()

        if not line:
            return zone_metadata

        nb_pair_bracket: int = 0
        for c in line:
            if c == "[" or c == "]":
                nb_pair_bracket += 1
        if nb_pair_bracket != 2 or not line.endswith("]"):
            raise ParsingError(
                "The metedata must be between [], "
                "and it should be only have one [] in the line"
            )

        line = line.strip("[]")
        print(f"line: {line}")
        for data in line.split():
            metadata: list[str] = data.split("=")
            if len(metadata) != 2:
                raise ParsingError(
                    f"Missing or invalid value for the metadata {
                        metadata[0]}, got: {metadata}")
            key: str = metadata[0]
            value: str = metadata[1]

            match key:
                case "zone":
                    state = ZoneMetadata.set_state_or_none(value)
                    if not state:
                        raise ParsingError(
                            "Zone state must be "
                            "(priority, restricted, normal, blocked), "
                            f"got: {value}"
                        )

                    zone_metadata.state = state
                case "color":
                    zone_metadata.color = value
                case "max_drones":
                    try:
                        max_drones = int(value)

                        if max_drones <= 0:
                            raise ParsingError(
                                "max_drones must be a positive integer, "
                                f"got: {max_drones}")
                        zone_metadata.max_drones = max_drones

                    except ValueError as e:
                        raise ValueError(
                            "max_drones must be a positive integer, "
                            f"got: {e}")
                case _:
                    raise ParsingError("Zone metadata field must be "
                                       "(zone=, color=, max_drones=), "
                                       f"got: {key}")
        return zone_metadata

    def _parse_zone(self, line: str) -> Zone:
        zone_data: list[str] = line.split(":")[1].rstrip().split()

        if not zone_data:
            raise ParsingError(
                "hub format: hub: name x y [metadata], "
                f"got: {zone_data}")

        name: str = zone_data[0]

        if name[0].isdigit():
            raise ParsingError(
                f"Error at line {self._current_line + 1}, "
                f"Missing or invalid hub's name, got: {name}")

        if " " in name or "-" in name:
            raise ParsingError("The name cannot contains spaces or dashes, "
                               f"got: {name}")
        try:
            x: int = int(zone_data[1])
            y: int = int(zone_data[2])
        except ValueError as e:
            raise ValueError(
                f"Hub coordinate must be positive integer, got: {e}")

        metadata_str: str = ""

        if len(zone_data) > 3:
            metadata_str = " ".join(zone_data[3:])

        metadata: ZoneMetadata = self._parse_zone_metadata(metadata_str)
        return Zone(name, x, y, metadata)

    def _parse_connection_metadata(self, line: str) -> int:
        nb_pair_bracket: int = 0

        for c in line:
            if c == "[" or c == "]":
                nb_pair_bracket += 1

        if nb_pair_bracket != 2 or not line.endswith("]"):
            raise ParsingError(
                "The metedata must be between [], "
                "and it should be only have one [] in the line"
            )

        line = line.strip("[]")
        data: list[str] = line.split("=")

        if data[0].strip() != "max_link_capacity":
            raise ParsingError(
                "Connection metadata format: "
                "max_link_capacity: X (where X is a positive integer), "
                f"got: {data[0]}")

        if len(data) == 2:
            try:
                max_link_capacity: int = int(data[1])

                if max_link_capacity <= 0:
                    raise ValueError(
                        "max_link_capacity must be a positive interger.")

            except ValueError as e:
                raise ValueError(f"max_link_capacity: {e}")
        else:
            raise ParsingError(
                f"the name must be max_link_capacity, got: {
                    data[1]}")

        return max_link_capacity

    def _parse_connection(self, line: str) -> Connection:
        connection_data: list[str] = line.split(":")[1].rstrip().split()

        if not connection_data:
            raise ParsingError(
                "Connection format: connection: "
                "zone1-zone2 [max_link_capacity: X "
                "(where X is a positive integer) (Optional)], "
                f"got: {connection_data}"
            )

        zones_name: list[str] = connection_data[0].split("-")

        if len(zones_name) != 2 or len(connection_data) > 2:
            raise ParsingError(
                "Connection format: zone1-zone2 [max_link_capacity: X "
                "(where X is a positive integer) (Optional)], "
                f"got: {connection_data}"
            )

        try:
            start: Zone = self._zones[zones_name[0]]
            dest: Zone = self._zones[zones_name[1]]
        except KeyError as e:
            raise ParsingError(f"The {e} hub has not been defined previously")

        if len(connection_data) == 2:
            max_link_capacity = self._parse_connection_metadata(
                connection_data[1])
            return Connection(start, dest, max_link_capacity)

        return Connection(start, dest)

    def parse(self) -> (
            dict[str, int | Zone | list[Zone] | list[Connection]]
    ):
        data: dict[str, int | Zone | list[Zone] | list[Connection]] = {}

        for line in self._file_lines:
            if not line.strip() or line.startswith("#"):
                self._current_line += 1
                continue

            if line.startswith("nb_drones: "):
                try:
                    nb_drones: int = self._get_nb_drones(line)
                except (ValueError, ParsingError) as e:
                    raise e

                data["nb_drones"] = nb_drones
                self._current_line += 2
                break

            raise ParsingError("The first line must contain nb_drones: X "
                               "(where X is a positive integer)")

        for line in self._file_lines[self._current_line:]:
            if not line.strip() or line.startswith("#"):
                self._current_line += 1
                continue

            if line.startswith("hub: "):
                zone = self._parse_zone(line)
                self._zones[zone.name] = zone

            elif line.startswith("connection: "):
                connection = self._parse_connection(line)

                for conn in self._connections:
                    if connection == conn:
                        raise ParsingError(
                            f"Error at line {self._current_line + 1}, "
                            "The connection must be unique.")

                self._connections.append(connection)

            elif line.startswith("start_hub: "):
                zone = self._parse_zone(line)
                self._zones[zone.name] = zone
                data["start_hub"] = zone

            elif line.startswith("end_hub: "):
                zone = self._parse_zone(line)
                self._zones[zone.name] = zone
                data["end_hub"] = zone

            elif line.startswith("nb_drones: "):
                raise ParsingError(
                    "The variable `nb_drones` has already been declared.")

            else:
                raise ParsingError(
                    f"Error at line {self._current_line + 1}.\n"
                    "The file must only contains the following names "
                    "(start_hub, end_hub, hub, connection) "
                    "and must be following with :space\n"
                    f"Got: {line}")
            self._current_line += 1
        try:
            data["start_hub"]
            data["end_hub"]
        except KeyError as e:
            raise ParsingError(f"The {e} is not declared.")

        for zone in self._zones.values():
            zone.add_connection(self._connections, self._zones)

        return data
