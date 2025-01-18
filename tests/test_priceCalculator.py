import pytest

from dopc.tools.priceCalculator import geoDistance

def test_geoDistance():
    coord1 = (60.17094, 24.93087)
    coord2 = (60.17094, 24.93087)

    distance = geoDistance(coord1, coord2)
    assert distance == 0

    coord1 = (60.17094, 24.93087)
    coord2 = (60.17012143, 24.92813512)

    expected_distance = 177
    distance = geoDistance(coord1, coord2)

    assert distance == expected_distance
