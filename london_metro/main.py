from london_metro import MetroGraph, read_data, dijkstra_search, App, reconstruct_path, ExtendedComboBox, create_summary
from datetime import time
import sys
from PyQt5.QtWidgets import QApplication


def main():
    connections, line_stations = read_data("../data/London_Underground_data.xlsx")
    metro_graph = MetroGraph()
    for line, station in line_stations:
        metro_graph.add_station(station, line)
    for line, source, destination, eta in connections:
        metro_graph.add_connection(line, source, destination, eta)

    app = QApplication(sys.argv)
    form = App(metro_graph)
    form.show()
    app.exec()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
