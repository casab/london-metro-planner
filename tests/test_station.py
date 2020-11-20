import pytest
from london_metro import Station
from datetime import time


class TestStation:
    @pytest.fixture(autouse=True)
    def create_tester(self):
        self._tester = Station("test_station", "test_line")

    def test_add_get_neighbor(self):
        test_neighbor = Station("test_neighbor", "test_line")
        self._tester.add_neighbor("test_line", test_neighbor, 0)
        assert ("test_line", test_neighbor) in self._tester.get_neighbors().keys()

    def test_add_get_line(self):
        self._tester.add_line("test_line2")
        assert "test_line2" in self._tester.get_lines()

    def test_get_name(self):
        assert "test_station" == self._tester.get_name()

    def test_get_eta(self):
        test_neighbor = Station("test_neighbor", "test_line")
        self._tester.add_neighbor("test_line", test_neighbor, 4)
        assert 4 == self._tester.get_eta("test_line", test_neighbor, time(12,34))
