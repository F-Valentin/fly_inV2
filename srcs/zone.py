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
                 color: str = "ESC[33m", max_drones: int = 1
                 ) -> None:
        self.state = state
        self.color = color
        self.max_drones = max_drones

    @staticmethod
    def set_state_or_none(zone_state: str) -> ZoneState | None:
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
        self.name: str = name
        self.x = x
        self.y = y
        self.metadata = metadata
        self.connections = connections if connections is not None else []
        self.nb_drones = 0

    def add_connection(self,
                       connections: list["Connection"],
                       zones: dict[str, "Zone"]
                       ) -> None:
        from connection import Connection
        for connection in connections:
            if self.name == connection.start.name:
                self.connections.append(connection)
                dest = zones[connection.dest.name]
                dest.connections.append(
                    Connection(
                        dest,
                        self,
                        connection.max_link_capacity))

    def get_cost_or_none(self) -> int | None:
        match self.metadata.state:
            case ZoneState.NORMAL | ZoneState.PRIORITY:
                return 1
            case ZoneState.RESTRICTED:
                return 2
            case _: return None
