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
    assert res=={'msge': f'failed getting venue info from {venue.dynamic_url}'}