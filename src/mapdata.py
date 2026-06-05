from dataclasses import dataclass
from typing import Optional


class ParsingError(Exception):
    pass


@dataclass(frozen=True)
class Metadata():
    zone_type: str = "normal"
    color: Optional[str] = None
    max_drones: int = 1
    max_capacity: int = 1


@dataclass(frozen=True)
class Zone():
    name: str
    x: int
    y: int
    metadata: Metadata

    def __post_init__(self) -> None:
        allowed_types = ["normal", "blocked", "restricted", "priority"]
        if self.metadata.zone_type not in allowed_types:
            raise ParsingError(f"Invalid type zone: {self.zone_type}")
        if self.metadata.max_drones <= 0:
            raise ParsingError("max_drone needs to be a positive integer.")


@dataclass(frozen=True)
class Connection:
    source: str
    destination: str
    metadata: Metadata
