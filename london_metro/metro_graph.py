from london_metro import Station
from typing import Dict, Optional, List


class MetroGraph:
    def __init__(self):
        """
        Creates a MetroGraph Graph
        """
        self.station_dict = {}

    def __iter__(self):
        return iter(self.station_dict.values())

    def add_station(self, name: str, line: str) -> Station:
        if name == "Stockwell":
            pass
        if name in self.station_dict.keys():
            self.station_dict[name].add_line(line)
            return self.station_dict[name]
        else:
            new_station = Station(name, line)
            self.station_dict[name] = new_station
            return new_station

    def get_station(self, name: str) -> Optional[Station]:
        if name in self.station_dict:
            return self.station_dict[name]
        else:
            return None

    def get_neighbors(self, name: str) -> Dict[Station, int]:
        return self.get_station(name).get_neighbors()

    def add_connection(self, line: str, source: str, destination: str, eta: int):
        if source not in self.station_dict:
            self.add_station(source, line)
        if destination not in self.station_dict:
            self.add_station(destination, line)

        self.station_dict[source].add_neighbor(self.station_dict[destination], eta)
        self.station_dict[destination].add_neighbor(self.station_dict[source], eta)

    def get_stations(self) -> List[Station]:
        return list(self.station_dict.keys())

    def __len__(self):
        return len(self.station_dict)
