from mapdata import ParsingError
from simulation import Simulation
from parsing import MapParser


def main() -> None:
    maps = [
            "./maps/easy/03_basic_capacity.txt"
            ]
    parser = MapParser()
    try:
        for map in maps:
            parser.parse(map)
            simulation = Simulation(
                zone=parser.zones,
                connection=parser.connections,
                drone_nb=parser.drones_nb
            )
            # simulation.print_graph()
            turn = 0
            while not simulation.all_drones_arrived():
                simulation.step()
                turn += 1
                print(f"Turn {turn}: {simulation.drone_state}")
    except ParsingError as e:
        print(f"ParsingError: {e}")


if __name__ == "__main__":
    main()
