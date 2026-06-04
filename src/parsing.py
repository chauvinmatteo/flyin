from mapdata import Zone, Connection


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

                start = line.find('[')
                metadata = ""
                if start != -1:
                    end = line.find(']')
                    metadata = line[start + 1: end]
                    data = line[:start].strip()
                else:
                    data = line
                parts = data.split()
                metadata_dict = {}
                if metadata:
                    for part in metadata.split():
                        key, value = part.split('=')
                        if key == 'max_drones':
                            metadata_dict[key] = int(value)
                        else:
                            metadata_dict[key] = value
                name, x, y = parts[1], int(parts[2]), int(parts[3])
                zone = Zone(name=name, x=x, y=y, **metadata_dict)
                print(zone)


def main() -> None:
    map = "./maps/easy/02_simple_fork.txt"
    parser = MapParser()
    parser.parse(map)


if __name__ == "__main__":
    main()
