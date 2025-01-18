import sys
import numpy as np
import geopy.distance
from dopc.tools.Venue import Venue



query_inputs = {'venue_slug': 'home-assignment-venue-helsinki', 'cart_value': 1000, 'user_lat':60.17094, 'user_lon': 24.93087}




def geoDistance(coord1: tuple, coord2: tuple) -> float:
    distance = geopy.distance.geodesic(coord1, coord2).m
    #d = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
    return int(np.round(distance))

def __call__(query_inputs: dict,
            static_info: dict,
            dynamic_info: dict) -> dict[str, float]:
    venue = Venue(venue_slug=query_inputs.get('venue_slug'))
    response = venue.getDynamicIfo()
    dynamicInfo= venue.parseVenueDynamicInfo(response)

    response = venue.getStaticicIfo()
    staticInfo= venue.parseVenueStaticInfo(response)
    x1 = query_inputs.get('user_lat')
    y1 = query_inputs.get('user_lon')
    x2 = staticInfo.get('COORDINATES')[1]
    y2 =  staticInfo.get('COORDINATES')[0]
    distance = geoDistance((x1, y1), (x2, y2))
    return {'price': 10}
