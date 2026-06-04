from dataclasses import dataclass
from typing import Optional


class ParsingError(Exception):
    pass


@dataclass
class Zone():
    name: str
    x: int
    y: int
    zone_type: str = "normal"
    color: Optional[str] = None
    max_drones: int = 1

    def __post_init__(self) -> None:
        allowed_types = ["normal", "blocked", "restricted", "priority"]
        if self.zone_type not in allowed_types:
            raise ParsingError(f"Invalid type zone: {self.zone_type}")
        if self.max_drones <= 0:
            raise ParsingError("max_drone needs to be a positive integer.")


@dataclass
class Connection:
    source: str
    destination: str
    max_capacity: int = 1
