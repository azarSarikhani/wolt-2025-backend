import sys
import numpy as np
import geopy.distance
from dopc.tools.Venue import Venue
from logging import Logger
from dopc.tools.logs import getConsoleLoger

calculatorLogger: Logger = getConsoleLoger('app')


def geoDistance(coord1: tuple, coord2: tuple) -> float:
    distance = geopy.distance.geodesic(coord1, coord2).m
    return int(np.round(distance))


def getRangesParams(distance: int, ranges: list) -> tuple[int]:
    for item in ranges:
        if distance >= item.get('min') and distance < item.get('max'):
            params = (item.get('a'), item.get('b'), item.get('max'))
            return params
    return (0, 0, 0)


def priceCalculator(query_inputs: dict,
                    static_info: dict,
                    dynamic_info: dict) -> tuple:
    x1 = query_inputs.get('user_lat')
    y1 = query_inputs.get('user_lon')
    x2 = static_info.get('COORDINATES')[1]
    y2 = static_info.get('COORDINATES')[0]
    distance = geoDistance((x1, y1), (x2, y2))

    base_price = dynamic_info.get('BASE_PRICE')
    distance_ranges = dynamic_info.get('DISTANCE_RANGES')
    a, b, _max = getRangesParams(distance, distance_ranges)
    if _max == 0:
        price = None
        return distance, price
    else:
        price = base_price + a + b * distance / 10
        return distance, np.round(price)
