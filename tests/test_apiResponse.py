# from src.app import app
# from fastapi.testclient import TestClient

from dopc.tools.Venue import Venue


def test_validRequestResponseSchema():
    venue = Venue(venue_slug='home-assignment-venue-helsinki')
    res = venue.getDynamicIfo()
    assert isinstance(res, dict)
