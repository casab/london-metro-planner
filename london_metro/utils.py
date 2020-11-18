from openpyxl import load_workbook


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
    rows = wb.values
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
    connections = [row for row in rows if (row[2] and row[3])]
    line_stations = [(row[0], row[1]) for row in rows if (row[2] is None and row[3] is None)]
    return connections, line_stations
