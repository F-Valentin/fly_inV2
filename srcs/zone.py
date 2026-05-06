from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from connection import Connection  # This is for the linter


class ZoneState(Enum):
    NORMAL = 0,
    PRIORITY = 1,
    RESTRICTED = 2,
    BLOCKED = 3,


class ZoneMetadata:
    def __init__(self, state: ZoneState = ZoneState.NORMAL, color: str = "ESC[33m",
                 max_drones: int = 1) -> None:
        self.state = state
        self.color = color
        self.max_drones = max_drones


class Zone:
    def __init__(self, name: str, x: int, y: int,
                 metadata: ZoneMetadata, connections: list[Connection] | None = None) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.metadata = metadata
        self.connections = connections if connections is not None else []
        self.nb_drones = 0
