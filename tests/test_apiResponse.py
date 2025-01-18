# from src.app import app
# from fastapi.testclient import TestClient

from dopc.tools.Venue import Venue


def test_validVenueResposne():
    venue = Venue(venue_slug='home-assignment-venue-helsinki')
    res = venue.getDynamicIfo()
    assert isinstance(res, dict)


def test_notFoundVenue():
    venue = Venue(venue_slug='home-assignment-venue-planet-shlorp')
    res = venue.getDynamicIfo()
    assert res == {'msge': f'failed getting venue info from {venue.dynamic_url}'}


def test_parseVenueDynamicInfo():
    venue = Venue(venue_slug='home-assignment-venue-helsinki')
    response = venue.getDynamicIfo()
    result = venue.parseVenueDynamicInfo(response)
    for item in ['ORDER_MINIMUM_NO_SURCHARGE', 'BASE_PRICE', 'DISTANCE_RANGES']:
        assert item in result.keys()
