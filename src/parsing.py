from mapdata import (Zone, Connection, ParsingError, ConnMetadata,
                     ZoneMetadata, Map)
from simulation import Simulation


class MapParser():
    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.raw_conn = []
        self.seen_conn = set()

    def parse(self, map: str) -> None:

        with open(map) as file:

            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if not line.startswith(('start_hub', 'end_hub', 'hub',
                                        'connection', 'nb_drones')):
                    continue
                if line.startswith('nb_drones'):
                    key, value = line.split(':')
                    try:
                        drone_nb = int(value)
                    except ValueError:
                        raise ParsingError(f"{value} is not an integer.")
                if line.startswith(('start_hub', 'end_hub', 'hub')):
                    start: int = line.find('[')
                    metadata: str = ""
                    if start != -1:
                        end: int = line.find(']')
                        metadata = line[start + 1: end]
                        data: str = line[:start].strip()
                    else:
                        data = line
                    parts: list[str] = data.split()
                    metadata_dict: dict = {}
                    if metadata:
                        for part in metadata.split():
                            key, value = part.split('=')
                            if key == 'max_drones':
                                try:
                                    metadata_dict[key] = int(value)
                                except ValueError:
                                    raise ParsingError(f"{key} value has to be"
                                                       "an integer.")
                            else:
                                metadata_dict[key] = value
                    allowed_meta = {'zone_type', 'color', 'max_drones'}
                    self.validate_meta(metadata_dict, allowed_meta, "Zone")
                    meta_obj = ZoneMetadata(**metadata_dict)
                    name, x, y = parts[1], int(parts[2]), int(parts[3])
                    zone = Zone(name=name, x=x, y=y, metadata=meta_obj)
                    # print(zone)
                    self.zones[name] = zone
                elif line.startswith('connection'):
                    self.raw_conn.append(line)
        self._process_conn()
        map_data = Map(nb_drones=drone_nb, zones=self.zones,
                       connections=self.connections)
        print(map_data)

    def _process_conn(self) -> None:

        for line in self.raw_conn:
            start = line.find('[')
            metadata = ""
            if start != -1:
                end = line.find(']')
                metadata = line[start + 1: end]
                data = line[:start].strip()
            else:
                data = line
            header, content = data.split(':', 1)
            parts = content.split('-')
            if len(parts) != 2:
                raise ParsingError("Zone's name can't have a dash in it.")
            metadata_dict = {}
            if metadata:
                for part in metadata.split():
                    key, value = part.split('=')
                    if key == 'max_link_capacity':
                        try:
                            metadata_dict[key] = int(value)
                        except ValueError:
                            raise ParsingError(f"{key} value has to be an"
                                               "integer.")
                    else:
                        raise ParsingError(f"{key} not allowed")
            meta_obj = ConnMetadata(**metadata_dict)
            first, second = parts[0].strip(), parts[1].strip()
            if first not in self.zones or second not in self.zones:
                raise ParsingError("Connection between unknown zone:"
                                   f"{first} or {second}")
            conn = Connection(source=first, destination=second,
                              metadata=meta_obj)
            self.connections.append(conn)
            # print(conn)

    def validate_meta(self, raw_dict, allowed_keys, context):

        for key in raw_dict.keys():
            if key not in allowed_keys:
                raise ParsingError(f"invalide {key} in context: {context}")
        return raw_dict


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
                drone_nb=4
            )
            simulation.print_graph()
    except ParsingError as e:
        print(f"ParsingError: {e}")


if __name__ == "__main__":
    main()
