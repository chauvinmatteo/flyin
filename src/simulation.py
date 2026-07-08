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
        for drone_id in self.drone_state:
            self.drones_in_zone["start"].append(drone_id)
        self.dist_map = self.compute_dijkstra_costs(self.goal)
        self.drones_path: dict[int, list[str]] = {}

    def get_connection(self, source: str, target: str) -> Connection:
        for conn in self.connection:
            if (conn.source == source and conn.destination == target) or \
               (conn.source == target and conn.destination == source):
                return conn
        return None

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

    def get_best_move(self, drone_current_zone: str, next_occ: str) -> str:
        best_score = float('inf')
        best_move = None

        for neighbor in self.graph[drone_current_zone]:
            zone_data = self.zone[neighbor]
            nb_drones = next_occ.get(neighbor, 0)
            max_drones = zone_data.metadata.max_drones
            new_cost = (nb_drones / max_drones) * 100.0
            g = self._get_weight(neighbor) + new_cost
            h = self.dist_map.get(neighbor, float('inf'))
            f = g + h
            dist_neighbor = self.dist_map.get(neighbor, float('inf'))
            dist_current = self.dist_map.get(drone_current_zone, float('inf'))
            if dist_neighbor >= dist_current:
                f += 500.0
            if f < best_score:
                best_score = f
                best_move = neighbor

        return best_move if best_move is not None else drone_current_zone

    def move_drone(self, drone_id: int, target_zone: str) -> None:
        old_zone = self.drone_state[drone_id]

        if drone_id in self.drones_in_zone[old_zone]:
            self.drones_in_zone[old_zone].remove(drone_id)
        self.drones_in_zone[target_zone].append(drone_id)
        self.drone_state[drone_id] = target_zone

    def step(self) -> None:

        future_occupancy = {name: len(self.drones_in_zone[name])
                            for name in self.graph}
        link_usage = {}
        drone_ids = sorted(self.drone_state.keys())

        for drone_id in drone_ids:
            current_zone = self.drone_state[drone_id]
            if current_zone == self.goal:
                continue
            target = self.get_best_move(current_zone, future_occupancy)
            if target == current_zone:
                continue
            conn = self.get_connection(current_zone, target)
            max_link = conn.metadata.max_link_capacity
            link_key = (current_zone, target)
            zone_data = self.zone[target]
            link_count = link_usage.get(link_key, 0)
            can_enter = (target == self.goal
                         or future_occupancy[target]
                         < zone_data.metadata.max_drones)
            can_pass = (link_count < max_link)

            if can_enter and can_pass:
                self.move_drone(drone_id, target)
                future_occupancy[current_zone] -= 1
                future_occupancy[target] += 1
                link_usage[link_key] = link_count + 1
            else:
                pass

    def all_drones_arrived(self) -> bool:
        return all(pos == self.goal for pos in self.drone_state.values())

    # def print_graph(self) -> None:
    #     for zone, voisins in self.graph.items():
    #         print(f"{zone} is link to : {', '.join(voisins)}")
    #     for zone in self.graph:
    #         best = self.get_best_move(zone)
    #         print(f"Depuis {zone}, le drone choisit d'aller vers : {best}")
    #     print(f"the goal is : {self.goal}")
    #     print(self.compute_dijkstra_costs(self.goal))
    #     print(self.drone_state)
