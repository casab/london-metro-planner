from typing import Dict, Set


class Station:
    def __init__(self, name, line):
        self.name = name
        self.lines: Set[str] = {line}
        self.neighbors: Dict["Station", int] = {}

    def add_neighbor(self, neighbor: "Station", eta: int):
        self.neighbors[neighbor] = eta

    def get_neighbors(self):
        return self.neighbors

    def add_line(self, line: str):
        self.lines.add(line)

    def get_lines(self):
        return self.lines

    def get_name(self) -> str:
        return self.name

    def get_eta(self, neighbor: "Station") -> int:
        return self.neighbors[neighbor]

    def __str__(self):
        return f"{self.name}\nNeighbors: {[x for x in self.neighbors]}\nLines: {[x for x in self.lines]}"

    def __eq__(self, other: "Station"):
        return self.name.lower() == other.name.lower()

    def __hash__(self):
        return hash(self.name.lower())

    def __lt__(self, other):
        return False
