from london_metro import *
import heapq
from typing import Dict, Optional, List, Tuple


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, Station]] = []

    def empty(self) -> bool:
        return len(self.elements) == 0

    def put(self, item: Station, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> Station:
        return heapq.heappop(self.elements)[1]


def dijkstra_search(start: Station, end: Station):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: Dict[Station, Optional[Station]] = {start: None}
    cost_so_far: Dict[Station, float] = {start: 0}

    while not frontier.empty():
        current: Station = frontier.get()

        if current == end:
            break

        for next_station, cost in current.get_neighbors().items():
            new_cost = cost_so_far[current] + cost
            if next_station not in cost_so_far or new_cost < cost_so_far[next_station]:
                cost_so_far[next_station] = new_cost
                priority = new_cost
                frontier.put(next_station, priority)
                came_from[next_station] = current

    return came_from, cost_so_far


def reconstruct_path(came_from: Dict[Station, Station],
                     start: Station, goal: Station) -> List[Station]:
    current: Station = goal
    path: List[Station] = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path
