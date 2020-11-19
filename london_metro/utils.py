from openpyxl import load_workbook
from typing import Set, Tuple, List


def read_data(path):
    """
    Reads the given excel file and returns the list of connections
    and dictionary of line stations
    :param path: String for the excel file to be read
    :return: (connections, line_stations)
             connections = Tuple(line name, source, destination, ETA)
             line_stations = Dictionary(line name: List(station))
    """
    wb = load_workbook(path)["Sheet1"]
    """
    line_stations = {}
    connections = [row for row in rows if (row[2] and row[3])]
    only_stations = [row for row in rows if (row[2] is None and row[3] is None)]
    for line, station, _, _ in only_stations:
        # This is a station information
        if line in line_stations.keys():
            line_stations[line].append(station)
        else:
            line_stations[line] = []
            line_stations[line].append(station)
    """
    connections: List[Tuple[str, str, str, int]] = [row for row in wb.values if (row[2] and row[3])]
    line_stations: List[Tuple[str, str]] = [(row[0], row[1]) for row in wb.values if (not row[2] and not row[3])]
    return connections, line_stations


def get_set_item(s: Set[str]) -> str:
    for e in s:
        return e
