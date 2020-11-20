from openpyxl import load_workbook
from typing import Dict, Tuple, List
from datetime import datetime, timedelta, time
from itertools import groupby
from london_metro import Station


def read_data(path):
    """
    Reads the given excel file and returns the list of connections
    and dictionary of line stations
    :param path: Path for the excel file to be read
    :return: To lists that represents connections and line-station pairs.
             Connection list structure is line, source, target, eta
             Line-station structure is line, station
    """
    wb = load_workbook(path)["Sheet1"]
    connections: List[Tuple[str, str, str, float]] = [row for row in wb.values if (row[2] and row[3])]
    line_stations: List[Tuple[str, str]] = [(row[0], row[1]) for row in wb.values if (not row[2] and not row[3])]
    return connections, line_stations


def add_minutes(time_obj: time, mins_to_add: float) -> time:
    """
    Adds the given minutes to the given time object and returns a new time object
    :param time_obj: time object to add minutes
    :param mins_to_add: total minutes to add
    :return: new time object with added minutes
    """
    fulldate = datetime(1, 1, 1, time_obj.hour, time_obj.minute, time_obj.second)
    fulldate = fulldate + timedelta(minutes=mins_to_add)
    return fulldate.time()


def calculate_steps(path: List[Tuple[Station, str]], cost_so_far: Dict[Station, float], leaving_time: time):
    """
    Analyzes the given path to create a list of steps in the form of;
        station, line, time to next station, total time
    """
    steps: List[List[str, str, float, float]] = []
    for i, (station, line) in enumerate(path):
        previous_line = None
        time_to_next = None
        if i < len(path) - 1:
            time_to_next = station.get_eta(line, path[i+1][0], add_minutes(leaving_time, cost_so_far[station]))
        if i > 1:
            previous_line = path[i - 1][1]
        if previous_line and (previous_line != line):
            steps.append([station.get_name(), previous_line, time_to_next, cost_so_far[station]])
        else:
            steps.append([station.get_name(), line, time_to_next, cost_so_far[station]])
    return steps


def calculate_changes(path: List[Tuple[Station, str]]):
    """
    Calculates when there is a line change, and returns a list of changes
    in the form of; [line, start station, end station]
    """
    changes = []
    for line, stations in groupby(path, lambda t: t[1]):
        stations = list(stations)
        start_station = stations[0][0].get_name()
        end_station = stations[-1][0].get_name()
        changes.append([line, start_station, end_station])
    for i in range(len(changes) - 1):
        changes[i][-1] = changes[i+1][1]
    return changes


def create_summary(path, cost_so_far, leaving_time):
    """
    Wrapper function around calculate_changes and calculate_steps
    """
    changes = calculate_changes(path)
    steps = calculate_steps(path, cost_so_far, leaving_time)
    return steps, changes
