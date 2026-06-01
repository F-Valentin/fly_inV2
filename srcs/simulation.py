from zone import Zone
from drone import Drone
from connection import Connection
from path import Path
from colors import ANSI


class SimulationError(Exception):
    pass


class Simulation:
    def __init__(self, end_hub: Zone) -> None:
        """Initialize simulation state for an end hub."""
        self.turn: int = 0
        self.active_connections: list[Connection] = []
        self.end_hub: Zone = end_hub

    def get_connection(self, start: Zone, dest: Zone) -> Connection | None:
        """Return the connection between start and dest if capacity allows."""
        for connection in start.connections:
            if connection.dest.name == dest.name:
                if (
                    len(connection.waiting_drones) <
                    connection.max_link_capacity
                ):
                    return connection
                break

        return None

    def _format_move(self, drone: Drone, start: Zone, dest: Zone) -> str:
        """Format a drone movement string with optional terminal color."""
        color_code = dest.metadata.color
        reset = ANSI["reset"] if color_code else ""

        dest_cost = dest.get_cost_or_none()

        if dest_cost is None:
            raise SimulationError("A drone cannot access a blocked zone")

        if dest_cost > 1:
            display = f"D{drone.id}-{start.name}-{dest.name}"
        else:
            display = f"D{drone.id}-{dest.name}"

        return f"{color_code}{display}{reset}"

    def _process_arrivals(self, drones: list[Drone]) -> list[Drone]:
        """Decrement waiting turns and land drones that have arrived."""
        finished_drones: list[Drone] = []

        for connection in self.active_connections:
            for drone in list(connection.waiting_drones):
                drone.waiting_turn -= 1

                if drone.waiting_turn <= 0:
                    dest = connection.dest
                    if (
                        dest.name == self.end_hub.name
                        or dest.nb_drones < dest.metadata.max_drones
                    ):
                        drone.status = "move"
                        connection.waiting_drones.remove(drone)
                        dest.nb_drones += 1

                        if dest.name == self.end_hub.name:
                            finished_drones.append(drone)

        return finished_drones

    def _process_departures(self, drones: list[Drone]) -> list[str]:
        """Move drones that are ready to depart onto their next connection."""
        movements: list[str] = []

        for drone in drones:
            if len(drone.path) <= 1:
                continue

            if drone.status == "waiting":
                continue

            start = drone.path[0]
            dest = drone.path[1]

            dest_cost = dest.get_cost_or_none()
            if dest_cost is None:
                raise SimulationError("A drone cannot access a blocked zone")

            drones_in_transit = sum(
                len(c.waiting_drones)
                for c in self.active_connections
                if c.dest.name == dest.name
            )

            if (
                dest.name != self.end_hub.name and
                dest.nb_drones + drones_in_transit >= dest.metadata.max_drones
            ):
                continue

            connection = self.get_connection(start, dest)
            if not connection:
                continue

            if connection not in self.active_connections:
                self.active_connections.append(connection)

            drone.waiting_turn = dest_cost
            connection.waiting_drones.append(drone)
            drone.status = "waiting"

            movements.append(self._format_move(drone, start, dest))

            if start.nb_drones > 0:
                start.nb_drones -= 1
            drone.path.pop(0)

        return movements

    def _print_zone_states(self, paths: list[Path]) -> None:
        """Print current occupancy for each zone and active connection."""
        all_drones: list[Drone] = [d for p in paths for d in p.drones]

        seen: set[str] = set()
        for path in paths:
            for zone in path.path:
                if zone.name in seen:
                    continue
                seen.add(zone.name)

                drones_in_zone = [
                    f"D{drone.id}"
                    for drone in all_drones
                    if (
                        drone.path and drone.path[0].name == zone.name and
                        drone.status != "waiting"
                    )
                ]

                if drones_in_zone:
                    color = ANSI.get(zone.metadata.color, "")
                    reset = ANSI["reset"] if color else ""
                    print(f"  {color}{zone.name}{reset}: {drones_in_zone}")

        for connection in self.active_connections:
            if connection.waiting_drones:
                in_transit = [f"D{d.id}" for d in connection.waiting_drones]
                print(
                    f"  {connection.start.name}->{connection.dest.name}"
                    f" (in transit): {in_transit}"
                )

    def simulation(self, drones: list[Drone], paths: list[Path]) -> int:
        """Run the simulation and return the total number of turns."""
        for path in paths:
            for drone in path.drones:
                drone.path.extend(path.path)

        while drones:
            finished = self._process_arrivals(drones)
            for d in finished:
                if d in drones:
                    drones.remove(d)

            moves = self._process_departures(drones)

            if moves:
                print(f"  moves : {' '.join(moves)}")
            self._print_zone_states(paths)

            if not drones:
                break

            self.turn += 1

        return self.turn
