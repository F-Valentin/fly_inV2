from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zone import Zone
    from drone import Drone


class Connection:
    def __init__(self, start: Zone, dest: Zone,
                 max_link_capacity: int = 1) -> None:
        """Initialize a connection between two zones with capacity."""
        self.start = start
        self.dest = dest
        self.max_link_capacity = max_link_capacity
        self.waiting_drones: list[Drone] = []

    def __eq__(self, other: object) -> bool:
        """Compare connections by endpoints, treating reverse links as equal."""
        if not isinstance(other, Connection):
            return NotImplemented

        if (self.start.name == other.dest.name and self.dest.name ==
                other.start.name):
            return True
        if (self.start.name == other.start.name and self.dest.name ==
                other.dest.name):
            return True

        return False
