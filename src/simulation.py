from mapdata import Zone, Connection


class Simulation():
    def __init__(self, zone: dict[str, Zone], connection: dict[Connection,
                                                               Connection],
                 drone_nb: int) -> None:
        self.zone: dict[str, Zone] = zone
        self.connection: dict[Connection, Connection] = connection
        self.drone_state: dict[int, str] = {i: "start" for i
                                            in range(1, drone_nb + 1)}

        self.graph = {name: [] for name in zone}
        for conn in connection:
            self.graph[conn.source].append(conn.destination)
            self.graph[conn.destination].append(conn.source)
        self.goal = [name for name, z in zone.items()
                     if z.role == "end_hub"][0]
        self.drones_path: dict[int, list[str]] = {}

    def compute_dijkstra_costs(self):
        pass

    def print_graph(self) -> None:
        print("--- Graphe d'adjacence ---")
        for zone, voisins in self.graph.items():
            print(f"{zone} est relié à : {', '.join(voisins)}")
        print(self.goal)
        print("--------------------------")
