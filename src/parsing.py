from mapdata import Zone, Connection, ParsingError


class MapParser():
    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []

    def parse(self, map: str) -> None:

        with open(map) as file:

            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if not line.startswith(('start_hub', 'end_hub', 'hub')):
                    continue

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
                                raise ParsingError(f"{key} value has to be an"
                                                   "integer.")
                        else:
                            metadata_dict[key] = value
                name, x, y = parts[1], int(parts[2]), int(parts[3])
                zone = Zone(name=name, x=x, y=y, **metadata_dict)
                self.zones[name] = zone
                print(zone)
            file.seek(0)

        with open(map) as file:

            for line in file:
                line = line.strip()
                if not line.startswith('connection'):
                    continue
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
                        if key == 'max_capacity':
                            try:
                                metadata_dict[key] = int(value)
                            except ValueError:
                                raise ParsingError(f"{key} value has to be an"
                                                   "integer.")
                first, second = parts[0].strip(), parts[1].strip()
                if first not in self.zones or second not in self.zones:
                    raise ParsingError("Connection between unknown zone:"
                                       f"{first} or {second}")
                connections = Connection(source=first, destination=second,
                                         **metadata_dict)
                self.connections.append(connections)
                print(connections)


def main() -> None:
    maps = [
            "./maps/easy/03_basic_capacity.txt"
            ]
    parser = MapParser()
    for map in maps:
        parser.parse(map)


if __name__ == "__main__":
    main()
