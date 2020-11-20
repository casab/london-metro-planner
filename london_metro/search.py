from london_metro import *
from heapq import heappush, heappop
from typing import Dict, Optional, List, Tuple
from datetime import time, timedelta


def dijkstra_search(start: Station, end: Station, leaving_time: time, waiting_time=1):
    priority_queue = []
    heappush(priority_queue, (0, start))
    came_from: Dict[Station, Optional[Tuple[Station, str]]] = {start: None}
    cost_so_far: Dict[Station, float] = {start: 0}

    while len(priority_queue):
        current: Station = heappop(priority_queue)[1]

        # Early stop the search
        if current == end:
            break

        for (line, next_station), cost in current.get_neighbors().items():
            new_cost = cost_so_far[current] + current.get_eta(line, next_station, add_minutes(leaving_time, cost_so_far[current])) + waiting_time
            if next_station not in cost_so_far or new_cost < cost_so_far[next_station]:
                cost_so_far[next_station] = new_cost
                priority = new_cost
                heappush(priority_queue, (priority, next_station))
                came_from[next_station] = current, line

    return came_from, cost_so_far


def reconstruct_path(came_from: Dict[Station, Tuple[Station, str]],
                     start: Station, goal: Station) -> List[Tuple[Station, str]]:
    current: Station = goal
    _, line = came_from[goal]
    path: List[Tuple[Station, str]] = []
    while current != start:
        path.append((current, line))
        current, line = came_from[current]
    start_line = path[-1][1]
    path.append((start, start_line))
    path.reverse()
    return path
