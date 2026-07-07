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
        self.drones_in_zone: dict[str, list[str]] = {name: [] for
                                                     name in self.graph}
        self.dist_map = self.compute_dijkstra_costs(self.goal)
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

    def get_best_move(self, drone_current_zone: str) -> str:
        best_score = float('inf')
        best_move = None
        for neighbor in self.graph[drone_current_zone]:
            zone_data = self.zone[neighbor]
            nb_drone = len(self.drones_in_zone[neighbor])
            max_drones = zone_data.metadata.max_drones
            new_cost = (nb_drone / max_drones) * 5.0
            g = self._get_weight(neighbor) + new_cost
            h = self.dist_map.get(neighbor, float('inf'))
            f = g + h
            if f < best_score:
                best_score = f
                best_move = neighbor
        return best_move if best_move is not None else drone_current_zone

    def print_graph(self) -> None:
        for zone, voisins in self.graph.items():
            print(f"{zone} is link to : {', '.join(voisins)}")
        for zone in self.graph:
            best = self.get_best_move(zone)
            print(f"Depuis {zone}, le drone choisit d'aller vers : {best}")
        print(f"the goal is : {self.goal}")
        print(self.compute_dijkstra_costs(self.goal))
