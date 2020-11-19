from london_metro import MetroGraph, read_data, breadth_first_search


def main():
    connections, line_stations = read_data("data/London_Underground_data.xlsx")
    metro_graph = MetroGraph()
    for line, station in line_stations:
        metro_graph.add_station(station, line)
    for line, source, destination, eta in connections:
        metro_graph.add_connection(line, source, destination, eta)

    source_dest = "Brixton"
    print(f'Reachable from {source_dest}:')
    came_from = breadth_first_search(metro_graph, source_dest)
    named_came_from = {k.get_name(): v.get_name() if v else None for k, v in came_from.items()}
    print(named_came_from)


if __name__ == "__main__":
    # TODO Location -> Node
    main()
