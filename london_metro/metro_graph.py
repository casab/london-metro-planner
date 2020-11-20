from london_metro import Station
from typing import Optional, List


class MetroGraph:
    def __init__(self):
        """
        Creates a MetroGraph Graph
        """
        self.station_dict = {}

    def add_station(self, name: str, line: str) -> Station:
        """
        Add a new station(Node) to the graph.
        """
        if name in self.station_dict.keys():
            # If the station is already added, then it means this entry
            # is on an another line. So add the new line to the previous Node
            self.station_dict[name.lower()].add_line(line)
            return self.station_dict[name.lower()]
        else:
            # Create a new station with the given name and metro line
            new_station = Station(name, line)
            # Add the new station to the graph
            self.station_dict[name.lower()] = new_station
            return new_station

    def get_station(self, name: str) -> Optional[Station]:
        """
        Searches and returns the Station with the given name
        If it's not fount, it returns None instead
        """
        if name.lower() in self.station_dict:
            return self.station_dict[name.lower()]
        else:
            return None

    def get_station_names(self) -> List[str]:
        """
        Returns a list of all the station names
        """
        return [station.get_name() for station in self.station_dict.values()]

    def add_connection(self, line: str, source: str, destination: str, eta: float):
        """
        Creates a connection between source and destination stations for the given line.
        Then the cost of traveling(estimated time) is added.
        """
        # If either of the stations are not available, they are created
        if source.lower() not in self.station_dict:
            self.add_station(source, line)
        if destination.lower() not in self.station_dict:
            self.add_station(destination, line)

        # A Edge is added to the graph by adding a neighbor to the stations(Nodes)
        self.station_dict[source.lower()].add_neighbor(line, self.station_dict[destination.lower()], eta)
        self.station_dict[destination.lower()].add_neighbor(line, self.station_dict[source.lower()], eta)

    def __len__(self):
        """
        Returns the number of stations in the graph
        """
        return len(self.station_dict)
