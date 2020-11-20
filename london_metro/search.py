from london_metro import *
from heapq import heappush, heappop
from typing import Dict, Optional, List, Tuple
from datetime import time


def dijkstra_search(start: Station, end: Station, leaving_time: time, waiting_time=1):
    """
    Implements Dijkstra's algorithm for MetroGraph
    """
    priority_queue = []
    # Insert the start point with the best priority(0) to the heapq
    heappush(priority_queue, (0, start))
    # came_from holds the previous station of every station that's searched
    # for the best cost
    came_from: Dict[Station, Optional[Tuple[Station, str]]] = {start: None}
    # cost_so_far hold the best total cost for every Station
    cost_so_far: Dict[Station, float] = {start: 0}
    while len(priority_queue):
        # Pops the Station with the lowest priority
        current: Station = heappop(priority_queue)[1]

        # Early stop the search
        if current == end:
            break

        for (line, next_station), cost in current.get_neighbors().items():
            # Calculates the time between the current station and the next station
            current_to_next_cost = current.get_eta(line, next_station, add_minutes(leaving_time, cost_so_far[current]))
            # Calculates the total cost for the next station
            new_cost = cost_so_far[current] + current_to_next_cost + waiting_time

            # If the cost of next station is not calculated or
            # if the new cost is better than before add the new cost to the cost_so_far
            # And insert the current station to the came_from dictionary
            if next_station not in cost_so_far or new_cost < cost_so_far[next_station]:
                cost_so_far[next_station] = new_cost
                priority = new_cost
                # Using a priority queue(heap queue) store the next station with the cost
                heappush(priority_queue, (priority, next_station))
                came_from[next_station] = current, line

    return came_from, cost_so_far


def reconstruct_path(came_from: Dict[Station, Tuple[Station, str]],
                     start: Station, goal: Station) -> List[Tuple[Station, str]]:
    """
    Reconstructs the path from start to end by analyzing the came_from dictionary
    from dijkstra_search
    :return: List of (station, line) pairs to construct a path
    """
    current: Station = goal
    _, line = came_from[goal]
    path: List[Tuple[Station, str]] = []
    # Iterate through came_from from end to start
    while current != start:
        path.append((current, line))
        current, line = came_from[current]
    # Append the start to the path with correct metro line
    start_line = path[-1][1]
    path.append((start, start_line))
    # Reverse the path to obtain start to end list.
    path.reverse()
    return path
