from london_metro import Station
from typing import Optional, List


class MetroGraph:
    def __init__(self):
        """
        Creates a MetroGraph Graph
        """
        self.station_dict = {}

    def __iter__(self):
        return iter(self.station_dict.values())

    def add_station(self, name: str, line: str) -> Station:
        if name in self.station_dict.keys():
            self.station_dict[name.lower()].add_line(line)
            return self.station_dict[name.lower()]
        else:
            new_station = Station(name, line)
            self.station_dict[name.lower()] = new_station
            return new_station

    def get_station(self, name: str) -> Optional[Station]:
        if name.lower() in self.station_dict:
            return self.station_dict[name.lower()]
        else:
            return None

    def add_connection(self, line: str, source: str, destination: str, eta: float):
        if source.lower() not in self.station_dict:
            self.add_station(source, line)
        if destination.lower() not in self.station_dict:
            self.add_station(destination, line)

        self.station_dict[source.lower()].add_neighbor(line, self.station_dict[destination.lower()], eta)
        self.station_dict[destination.lower()].add_neighbor(line, self.station_dict[source.lower()], eta)

    def __len__(self):
        return len(self.station_dict)
