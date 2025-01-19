import json
import pytest

from dopc.tools.Venue import Venue
from dopc.tools.priceCalculator import geoDistance, getRangesParams, priceCalculator

cases = [
    {"distance" : 100, "expected_params": (0, 0, 500)},
    {"distance" : 500, "expected_params": (100, 0, 1000)},
    {"distance" : 2000, "expected_params": (0, 0, 0)}
]

geo_coordinations_cases = [
	{'coord1': (60.17094, 24.93087),'coord2': (60.17094, 24.93087), 'expected_distance': 0},
	{'coord1': (60.17094, 24.93087),'coord2': (60.17012143, 24.92813512), 'expected_distance': 177}

]

query_inputs_cases = [
    {'query_inputs' : {'venue_slug': 'home-assignment-venue-helsinki', 'cart_value': 1000, 'user_lat':60.17094, 'user_lon': 24.93087}}
]

#static_info = {'COORDINATES': [24.92813512, 60.17012143]}
#dynamic_info = {'ORDER_MINIMUM_NO_SURCHARGE': 1000, 'BASE_PRICE': 190, 'DISTANCE_RANGES': [{'min': 0, 'max': 500, 'a': 0, 'b': 0.0, 'flag': None}, {'min': 500, 'max': 1000, 'a': 100, 'b': 0.0, 'flag': None}, {'min': 1000, 'max': 1500, 'a': 200, 'b': 0.0, 'flag': None}, {'min': 1500, 'max': 2000, 'a': 200, 'b': 1.0, 'flag': None}, {'min': 2000, 'max': 0, 'a': 0, 'b': 0.0, 'flag': None}]}


@pytest.fixture(scope="module", autouse=True)
def mock__static_dynamicInfo():
    with open('tests/dynamic_info.json') as data:
        dynamicInfo = json.load(data)
    with open('tests/static_info.json') as data:
        staticInfo = json.load(data)
    return dynamicInfo, staticInfo


@pytest.mark.parametrize("geo_coordinations_cases", geo_coordinations_cases)   
def test_geoDistance(geo_coordinations_cases):
    coord1 = geo_coordinations_cases.get('coord1')
    coord2 = geo_coordinations_cases.get('coord2')

    distance = geo_coordinations_cases.get('expected_distance')
    assert geoDistance(coord1, coord2) == distance 


@pytest.mark.parametrize("cases", cases)   
def test_rangesParams(cases, mock__static_dynamicInfo):
    dynamic_info = mock__static_dynamicInfo[0]
    distance_ranges = dynamic_info.get('DISTANCE_RANGES')
    distance = cases.get("distance")
    expected_params = cases.get("expected_params")

    assert expected_params == getRangesParams(distance, distance_ranges)


@pytest.mark.parametrize("query_inputs_cases", query_inputs_cases)   
def test_priceCalculator(query_inputs_cases, mock__static_dynamicInfo):
    dynamic_info, static_info = mock__static_dynamicInfo
    query_inputs = query_inputs_cases.get("query_inputs")
    distance_ranges = dynamic_info.get('DISTANCE_RANGES')
    distance, price = priceCalculator(query_inputs, static_info, dynamic_info )
    assert distance == 177
    assert price == 190