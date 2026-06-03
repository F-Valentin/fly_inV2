from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from connection import Connection


class ZoneState(Enum):
    NORMAL = 0,
    PRIORITY = 1,
    RESTRICTED = 2,
    BLOCKED = 3,


class ZoneMetadata:
    def __init__(self, state: ZoneState = ZoneState.NORMAL,
                 color: str = "", max_drones: int = 1
                 ) -> None:
        """Store metadata for a zone,
        including state, color, and capacity."""
        self.state = state
        self.color = color
        self.max_drones = max_drones

    @staticmethod
    def set_state_or_none(zone_state: str) -> ZoneState | None:
        """Convert a state string to the corresponding ZoneState enum."""
        match zone_state.strip().lower():
            case "normal":
                return ZoneState.NORMAL
            case "priority":
                return ZoneState.PRIORITY
            case "restricted":
                return ZoneState.RESTRICTED
            case "blocked":
                return ZoneState.BLOCKED
            case _:
                return None


class Zone:
    def __init__(self, name: str, x: int, y: int,
                 metadata: ZoneMetadata,
                 connections: list[Connection] | None = None
                 ) -> None:
        """Initialize a zone with coordinates,
        metadata, and optional connections."""
        self.name: str = name
        self.x = x
        self.y = y
        self.metadata = metadata
        self.connections = connections if connections is not None else []
        self.nb_drones = 0

    def add_connection(self,
                       connections: list["Connection"],
                       ) -> None:
        """Attach all outgoing connections for this zone."""
        for connection in connections:
            if self.name == connection.start.name:
                self.connections.append(connection)

    def get_cost_or_none(self) -> int | None:
        """Return the traversal cost for this zone,
        or None if blocked."""
        match self.metadata.state:
            case ZoneState.NORMAL | ZoneState.PRIORITY:
                return 1
            case ZoneState.RESTRICTED:
                return 2
            case _: return None
