from dataclasses import dataclass
from typing import Optional


class ParsingError(Exception):
    pass


@dataclass(frozen=True)
class ZoneMetadata():
    zone_type: str = "normal"
    color: Optional[str] = None
    max_drones: int = 1


@dataclass(frozen=True)
class ConnMetadata():
    max_link_capacity: int = 1


@dataclass(frozen=True)
class Zone():
    name: str
    x: int
    y: int
    metadata: ZoneMetadata

    def __post_init__(self) -> None:
        allowed_types = [
            "normal",
            "blocked",
            "restricted",
            "priority"
            ]
        if self.metadata.zone_type not in allowed_types:
            raise ParsingError(f"Invalid type zone: {self.metadata.zone_type}")
        if self.metadata.max_drones <= 0:
            raise ParsingError("max_drone needs to be a positive integer.")


@dataclass(frozen=True)
class Connection():
    source: str
    destination: str
    metadata: ConnMetadata

    def __post_init__(self) -> None:
        if self.metadata.max_link_capacity < 1:
            raise ParsingError("max_link_capacity can't be lower than one.")


@dataclass(frozen=True)
class Map():
    nb_drones: int
    zones: list[Zone]
    connections: list[Connection]
