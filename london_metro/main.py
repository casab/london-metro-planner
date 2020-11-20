from london_metro import MetroGraph, read_data, dijkstra_search, reconstruct_path, add_minutes
from datetime import time


def main():
    connections, line_stations = read_data("../data/London_Underground_data.xlsx")
    metro_graph = MetroGraph()
    for line, station in line_stations:
        metro_graph.add_station(station, line)
    for line, source, destination, eta in connections:
        metro_graph.add_connection(line, source, destination, eta)

    start = metro_graph.get_station("maida Vale")
    end = metro_graph.get_station("Westbourne park")
    leaving_time = time(13, 0)

    came_from, cost_so_far = dijkstra_search(start, end, leaving_time)
    path = reconstruct_path(came_from, start, end)

    print(f"Line                Station             Time to next    Total Time")
    for i, (station, line) in enumerate(path):
        next_line = None
        time_to_next = None
        if i < len(path) - 1:
            next_line = path[i + 1][1]
            time_to_next = station.get_eta(line, path[i+1][0], add_minutes(leaving_time, cost_so_far[station]))
        print(f"{line:20}{station.get_name():20}{(time_to_next or ''):12}{cost_so_far[station]:14}")
        if next_line and (next_line != line):
            print(f"-->Change to {next_line}<--")


if __name__ == "__main__":
    main()
