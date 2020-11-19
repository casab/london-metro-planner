from london_metro import MetroGraph, read_data, dijkstra_search, reconstruct_path


def main():
    connections, line_stations = read_data("data/London_Underground_data.xlsx")
    metro_graph = MetroGraph()
    for line, station in line_stations:
        metro_graph.add_station(station, line)
    for line, source, destination, eta in connections:
        metro_graph.add_connection(line, source, destination, eta)

    start = metro_graph.get_station("North Greenwich")
    end = metro_graph.get_station("Earl's Court")

    came_from, cost_so_far = dijkstra_search(start, end)
    path = reconstruct_path(came_from, start, end)

    print([station.get_name() for station in path])


if __name__ == "__main__":
    # TODO Location -> Node
    main()
