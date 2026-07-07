from mapdata import Zone, Connection
from collections import deque


class Simulation():
    def __init__(self, zone: dict[str, Zone], connection: dict[Connection,
                                                               Connection],
                 drone_nb: int) -> None:
        self.zone: dict[str, Zone] = zone
        self.connection: dict[Connection, Connection] = connection
        self.drone_state: dict[int, str] = {i: "start" for i
                                            in range(1, drone_nb + 1)}

        self.graph: dict[str, int] = {name: [] for name in zone}
        for conn in connection:
            self.graph[conn.source].append(conn.destination)
            self.graph[conn.destination].append(conn.source)
        self.goal = [name for name, z in zone.items()
                     if z.role == "end_hub"][0]
        self.drones_path: dict[int, list[str]] = {}

    def _get_weight(self, zone_name: str) -> float:
        zones = self.zone[zone_name]
        if zones.metadata.zone_type == "normal":
            return 1.0
        elif zones.metadata.zone_type == "blocked":
            return float('inf')
        elif zones.metadata.zone_type == "restricted":
            return 5.0
        elif zones.metadata.zone_type == "priority":
            return 0.1

    def compute_dijkstra_costs(self, goal: str) -> dict[str, float]:
        distances: dict[str, float] = {name: float('inf')
                                       for name in self.graph}
        distances[goal] = 0

        queue: deque[str] = deque([goal])

        while queue:
            current: str = queue.popleft()
            for neighbor in self.graph[current]:
                cost = self._get_weight(neighbor)
                if distances[neighbor] > distances[current] + cost:
                    distances[neighbor] = distances[current] + cost
                    queue.append(neighbor)
        return distances

    def print_graph(self) -> None:
        for zone, voisins in self.graph.items():
            print(f"{zone} is link to : {', '.join(voisins)}")
        print(f"the goal is : {self.goal}")
        print(self.compute_dijkstra_costs(self.goal))
