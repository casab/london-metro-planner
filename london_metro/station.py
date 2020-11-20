from typing import Dict, Set, Tuple
from datetime import time

FAST_LINES = {
    "bakerloo": [(time(9, 0), time(16, 0)), (time(19, 0), time(23, 59))]
}


class Station:
    def __init__(self, name, line):
        self.name = name
        self.lines: Set[str] = {line}
        self.neighbors: Dict[Tuple[str, "Station"], float] = {}

    def add_neighbor(self, line: str, neighbor: "Station", eta: float):
        self.neighbors[(line, neighbor)] = eta

    def get_neighbors(self):
        return self.neighbors

    def add_line(self, line: str):
        self.lines.add(line)

    def get_lines(self):
        return self.lines

    def get_name(self) -> str:
        return self.name

    def get_eta(self, line: str, neighbor: "Station", leaving_time: time) -> float:
        if line and line.lower() in FAST_LINES:
            faster = any(constraint[0] < leaving_time < constraint[1] for constraint in FAST_LINES[line.lower()])
            if faster:
                return self.neighbors[(line, neighbor)] / 2.0
        return self.neighbors[(line, neighbor)]

    def __str__(self):
        return f"{self.name}\nNeighbors: {[x for x in self.neighbors]}\nLines: {[x for x in self.lines]}"

    def __eq__(self, other: "Station"):
        return self.name.lower() == other.name.lower()

    def __hash__(self):
        return hash(self.name.lower())

    def __lt__(self, other):
        return False
