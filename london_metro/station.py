from typing import Dict, Set, Tuple
from datetime import time

# Define Fast lines with the constraints here
# the structure is;
#    line_name: [constrant1, constraint2, ...]
#    where contraint is (after, before)
FAST_LINES = {
    "bakerloo": [(time(9, 0), time(16, 0)), (time(19, 0), time(23, 59))]
}


class Station:
    """
    Defines a metro station(Node)
    """
    def __init__(self, name: str, line: str):
        self.name = name
        self.lines: Set[str] = {line}
        # Hold the connections(Edges) to other stations in a dictionary
        # The structure is like {(line, station): cost}
        self.neighbors: Dict[Tuple[str, "Station"], float] = {}

    def add_neighbor(self, line: str, neighbor: "Station", eta: float):
        """
        Add a new neighbor station to the current station.
        :param line: The name of the metro line
        :param neighbor: An another station
        :param eta: Estimated time of arrival in minutes
        :return: None
        """
        self.neighbors[(line, neighbor)] = eta

    def get_neighbors(self):
        """
        Returns all the neighbors of the current station.
        """
        return self.neighbors

    def add_line(self, line: str):
        """
        A same station can be on several metro lines.
        Secondary lines can be added with this method.
        :param line:
        :return:
        """
        self.lines.add(line)

    def get_lines(self):
        """
        Returns all the lines this station is on.
        """
        return self.lines

    def get_name(self) -> str:
        """
        Returns the name of the Station.
        :return:
        """
        return self.name

    def get_eta(self, line: str, neighbor: "Station", leaving_time: time) -> float:
        """
        Calculates the eta from the current station to an another neighbor station.
        """
        # Special case for faster lines
        if line and line.lower() in FAST_LINES:
            # Check if the conditions are fulfilled for faster lines
            faster = any(constraint[0] < leaving_time < constraint[1] for constraint in FAST_LINES[line.lower()])
            if faster:
                # Divide the cost to half since it's twice as fast
                return self.neighbors[(line, neighbor)] / 2.0
        # For all other cases, return the cost from neighbors dictionary
        return self.neighbors[(line, neighbor)]

    def __eq__(self, other: "Station"):
        """
        Defines how different stations can be equal or not.
        If two stations has the same case insensitive name,
        then they are equal.
        """
        return self.name.lower() == other.name.lower()

    def __hash__(self):
        """
        Calculates a hash from the name
        """
        return hash(self.name.lower())

    def __lt__(self, other):
        return False
