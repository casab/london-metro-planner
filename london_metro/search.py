from london_metro import *
from heapq import heappush, heappop
from typing import Dict, Optional, List


def dijkstra_search(start: Station, end: Station):
    priority_queue = []
    heappush(priority_queue, (0, start))
    came_from: Dict[Station, Optional[Station]] = {start: None}
    cost_so_far: Dict[Station, float] = {start: 0}

    while len(priority_queue):
        current: Station = heappop(priority_queue)[1]

        # Early stop the search
        if current == end:
            break

        for next_station, cost in current.get_neighbors().items():
            new_cost = cost_so_far[current] + cost
            if next_station not in cost_so_far or new_cost < cost_so_far[next_station]:
                cost_so_far[next_station] = new_cost
                priority = new_cost
                heappush(priority_queue, (priority, next_station))
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
