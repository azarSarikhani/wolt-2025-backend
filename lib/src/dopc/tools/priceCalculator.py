import sys
import numpy as np
import geopy.distance
from dopc.tools.Venue import Venue



query_inputs = {'venue_slug': 'home-assignment-venue-helsinki', 'cart_value': 1000, 'user_lat':60.17094, 'user_lon': 24.93087}




def geoDistance(coord1: tuple, coord2: tuple) -> float:
    distance = geopy.distance.geodesic(coord1, coord2).m
    return int(np.round(distance))


def getRangesParams(distance: int, ranges: list ) -> tuple[int]:
    for item in ranges:
        if distance >= item.get('min') and  distance < item.get('max'):
            params = (item.get('a'), item.get('b'), item.get('max'))
            return params
    return (0, 0, 0)


def priceCalculator(query_inputs: dict,
            static_info: dict,
            dynamic_info: dict) -> dict[str, float]:
    venue = Venue(venue_slug=query_inputs.get('venue_slug'))
    response_dynamic = venue.getDynamicIfo()
    dynamicInfo= venue.parseVenueDynamicInfo(response_dynamic)

    response_static = venue.getStaticicIfo()
    staticInfo= venue.parseVenueStaticInfo(response_static)
    x1 = query_inputs.get('user_lat')
    y1 = query_inputs.get('user_lon')
    x2 = staticInfo.get('COORDINATES')[1]
    y2 =  staticInfo.get('COORDINATES')[0]
    distance = geoDistance((x1, y1), (x2, y2))

    base_price = dynamicInfo.get('BASE_PRICE')
    distance_ranges = dynamicInfo.get('DISTANCE_RANGES')
    a, b, _max = getRangesParams(distance, distance_ranges)
    price = base_price + a + b * distance / 10
    return {'price': price}
