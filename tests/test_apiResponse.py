import pytest
from fastapi.testclient import TestClient

from dopc.app import app


client = TestClient(app)

def test_validRequestResponseSchema():
    response = client.get('/api/v1/delivery-order-price', 
               params = {'venue_slug': 'a', 'cart_value': 2, 'user_lat':2.1, 'user_lon': 3.1})
    assert response.status_code == 200
    assert response.json().get("delivery_fee") != None  # noqa: E711



