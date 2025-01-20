import numpy as np  # type: ignore
import geopy.distance  # type: ignore
from logging import Logger
from dopc.tools.logs import getConsoleLoger
from typing import Tuple

calculatorLogger: Logger = getConsoleLoger('app')


def geoDistance(coord1: tuple, coord2: tuple) -> int:
    distance = geopy.distance.geodesic(coord1, coord2).m
    return int(np.round(distance))


def getRangesParams(distance: int, ranges: list) -> Tuple[int, int, int]:
    for item in ranges:
        if distance >= item.get('min') and distance < item.get('max'):
            params = (item.get('a') or 0, item.get('b') or 0, item.get('max') or 0)
            return params
    return (0, 0, 0)


def priceCalculator(query_inputs: dict,
                    static_info: dict,
                    dynamic_info: dict) -> tuple:
    x1 = query_inputs.get('user_lat')
    y1 = query_inputs.get('user_lon')
    x2 = static_info['COORDINATES'][1]
    y2 = static_info['COORDINATES'][0]
    distance = geoDistance((x1, y1), (x2, y2))

    base_price = dynamic_info.get('BASE_PRICE') or 0
    distance_ranges = dynamic_info.get('DISTANCE_RANGES') or []
    a, b, _max = getRangesParams(distance, distance_ranges)
    if _max == 0:
        price = None
        return distance, price
    else:
        price = base_price + a + b * distance / 10
        return distance, np.round(price)
