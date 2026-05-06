from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zone import Zone


class Connection:
    def __init__(self, start: Zone, dest: Zone,
                 max_link_capacity: int = 1) -> None:
        self.start = start
        self.dest = dest
        self.max_link_capacity = max_link_capacity
        self.waiting_drones: list["Drone"] = []
