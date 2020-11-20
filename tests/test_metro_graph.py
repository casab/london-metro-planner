import pytest
from london_metro import MetroGraph, Station


class TestMetroGraph:
    @pytest.fixture(autouse=True)
    def create_tester(self):
        self._tester = MetroGraph()

    def test_add_get_station(self):
        test_station = Station("test_station", "test_line")
        self._tester.add_station("test_station", "test_line")
        assert test_station == self._tester.get_station("test_station")

    def test_add_get_case_insensitive_station(self):
        test_station = Station("Test_Station", "test_line")
        self._tester.add_station("Test_Station", "test_line")
        assert test_station == self._tester.get_station("test_station")

    def test_add_second_line(self):
        self._tester.add_station("test_station", "test_line1")
        self._tester.add_station("test_station", "test_line2")
        test_station = self._tester.get_station("test_station")
        assert {"test_line1", "test_line2"} == test_station.get_lines()

    def test_add_connection(self):
        self._tester.add_station("test_station1", "test_line")
        self._tester.add_station("test_station2", "test_line")
        test_station_1 = self._tester.get_station("test_station1")
        test_station_2 = self._tester.get_station("test_station2")
        self._tester.add_connection("test_line", "test_station1", "test_station2", 2)
        assert {("test_line", test_station_2): 2} == test_station_1.get_neighbors()

    def get_none_existing_connection(self):
        assert self._tester.get_station("test_station") is None
