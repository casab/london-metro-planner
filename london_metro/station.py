from typing import Dict, Set, Tuple


class Station:
    def __init__(self, name, line):
        self.name = name
        self.lines: Set[str] = {line}
        self.neighbors: Dict[Tuple[str, "Station"], int] = {}

    def add_neighbor(self, line: str, neighbor: "Station", eta: int):
        self.neighbors[(line, neighbor)] = eta

    def get_neighbors(self):
        return self.neighbors

    def add_line(self, line: str):
        self.lines.add(line)

    def get_lines(self):
        return self.lines

    def get_name(self) -> str:
        return self.name

    def get_eta(self, line: str, neighbor: "Station") -> int:
        return self.neighbors[(line, neighbor)]

    def __str__(self):
        return f"{self.name}\nNeighbors: {[x for x in self.neighbors]}\nLines: {[x for x in self.lines]}"

    def __eq__(self, other: "Station"):
        return self.name.lower() == other.name.lower()

    def __hash__(self):
        return hash(self.name.lower())

    def __lt__(self, other):
        return False
