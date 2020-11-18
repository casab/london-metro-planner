from london_metro import MetroGraph, read_data, breadth_first_search


def main():
    connections, line_stations = read_data("data/London_Underground_data.xlsx")
    metro_graph = MetroGraph()
    for line, station in line_stations:
        metro_graph.add_station(station, line)
    for line, source, destination, eta in connections:
        metro_graph.add_connection(line, source, destination, eta)

    print('Reachable from A:')
    breadth_first_search(metro_graph, "Brixton")


if __name__ == "__main__":
    # TODO Location -> Node
    main()
