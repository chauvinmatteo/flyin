from mapdata import ParsingError
from simulation import Simulation
from parsing import MapParser


def main() -> None:
    maps = [
            "./maps/challenger/01_the_impossible_dream.txt"
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
            while not simulation.all_drones_arrived():
                simulation.step()
                print(simulation.turn)
            print(simulation.turn)
    except ParsingError as e:
        print(f"ParsingError: {e}")


if __name__ == "__main__":
    main()
