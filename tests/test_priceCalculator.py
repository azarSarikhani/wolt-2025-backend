import pytest

from dopc.tools.priceCalculator import geoDistance, getRangesParams, priceCalculator

cases = [
    {"distance" : 100, "expected_params": (0, 0, 500)},
    {"distance" : 500, "expected_params": (100, 1, 1000)},
    {"distance" : 1000, "expected_params": (0, 0, 0)}
]

query_inputs_cases = [
    {'venue_slug': 'home-assignment-venue-helsinki', 'cart_value': 1000, 'user_lat':60.17094, 'user_lon': 24.93087}
]

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

@pytest.mark.parametrize("cases", cases)   
def test_rangesParams(cases):
    distance = cases.get("distance")
    expected_params = cases.get("expected_params")
    distance_ranges = [{
			"min": 0,
			"max": 500,
			"a": 0,
			"b": 0,
		},
		{
			"min": 500,
			"max": 1000,
			"a": 100,
			"b": 1,
		},
		{
			"min": 1000,
			"max": 0,
			"a": 0,
			"b": 0,
		}
	]
    assert expected_params == getRangesParams(distance, distance_ranges)
    
@pytest.mark.parametrize("cases", cases)   
def test_priceCalculator(cases):
    distance = cases.get("distance")
    expected_params = cases.get("expected_params")
    distance_ranges = [{
			"min": 0,
			"max": 500,
			"a": 0,
			"b": 0,
		},
		{
			"min": 500,
			"max": 1000,
			"a": 100,
			"b": 1,
		},
		{
			"min": 1000,
			"max": 0,
			"a": 0,
			"b": 0,
		}
	]
    assert expected_params == getRangesParams(distance, distance_ranges)