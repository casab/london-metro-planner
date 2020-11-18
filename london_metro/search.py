from london_metro import *
import collections
from typing import Dict


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
    reached: Dict[Station, bool] = {start: True}

    while not frontier.empty():
        current: str = frontier.get()
        print("  Visiting %s" % current.get_name())
        for next, cost in graph.get_neighbors(current.get_name()).items():
            if next not in reached:
                frontier.put(next)
                reached[next] = True

