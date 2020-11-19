import pytest
from london_metro import Station


@pytest.fixture
def tester():
    return Station("test_station", "test_line")


def test_add_get_neighbor(tester):
    test_neighbor = Station("test_neighbor", "test_line")
    tester.add_neighbor(test_neighbor, 0)
    assert test_neighbor in tester.get_neighbors().keys()


def test_add_get_line(tester):
    tester.add_line("test_line2")
    assert "test_line2" in tester.get_lines()


def test_get_name(tester):
    assert "test_station" == tester.get_name()


def test_get_eta(tester):
    test_neighbor = Station("test_neighbor", "test_line")
    tester.add_neighbor(test_neighbor, 4)
    assert 4 == tester.get_eta(test_neighbor)
