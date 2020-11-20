from openpyxl import load_workbook
from typing import Set, Tuple, List
from datetime import time, datetime, timedelta


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
    connections: List[Tuple[str, str, str, float]] = [row for row in wb.values if (row[2] and row[3])]
    line_stations: List[Tuple[str, str]] = [(row[0], row[1]) for row in wb.values if (not row[2] and not row[3])]
    return connections, line_stations


def get_set_item(s: Set[str]) -> str:
    for e in s:
        return e


def add_minutes(time_obj, mins_to_add):
    fulldate = datetime(1, 1, 1, time_obj.hour, time_obj.minute, time_obj.second)
    fulldate = fulldate + timedelta(minutes=mins_to_add)
    return fulldate.time()
