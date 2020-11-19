from london_metro import *
import collections
from typing import Dict, Optional


class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self) -> bool:
        return len(self.elements) == 0

    def put(self, x: Station):
        self.elements.append(x)

    def get(self) -> Station:
        return self.elements.popleft()


def breadth_first_search(graph: MetroGraph, name: str):
    # print out what we find
    frontier = Queue()
    start = graph.get_station(name)
    frontier.put(start)
    came_from: Dict[Station, Optional[Station]] = {start: None}
    """
    current_lines = start.get_lines()
    current_line = get_set_item(current_lines)
    print(f"Currently on line {current_line}")
    """
    while not frontier.empty():
        current: Station = frontier.get()
        print(f"  Visiting {current.get_name()}")
        for next_station, cost in current.get_neighbors().items():
            if next_station not in came_from:
                """
                # TODO: this needs fixing
                if current_line not in (current_lines & next_station.get_lines()):
                    print(f"**Current line: {current_line}")
                    print(f"**Current lines: {current_lines}")
                    print(f"**Next lines: {next_station.get_lines()}")
                    current_line = get_set_item(next_station.get_lines())
                    print(f"Changed current line to {current_line}")
                    current_lines = next_station.get_lines()
                """
                frontier.put(next_station)
                came_from[next_station] = current
    return came_from
