from london_metro import MetroGraph, read_data, App, resource_path
import sys
from PyQt5.QtWidgets import QApplication


def main():
    # Read and parse the data from the excel file
    connections, line_stations = read_data(resource_path("London_Underground_data.xlsx"))

    # Create a Graph
    metro_graph = MetroGraph()
    # Add every stations(Nodes) and connections(Edges) to the graph
    for line, station in line_stations:
        metro_graph.add_station(station, line)
    for line, source, destination, eta in connections:
        metro_graph.add_connection(line, source, destination, eta)

    # Create a PyQT Gui application
    q_app = QApplication(sys.argv)

    # Pass the graph to the QT application
    app = App(metro_graph)
    app.show()
    q_app.exec()

    sys.exit(q_app.exec_())


if __name__ == "__main__":
    main()
