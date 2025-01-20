import pytest
from fastapi.testclient import TestClient

from app.app import app


client = TestClient(app)


# @pytest.mark.skip(reason="debugging test")
def test_badRequestResponseCode():
    response = client.get('/api/v1/delivery-order-price',
                          params={'venue_slug': 'home-assignment-venue-helsinki', 'cart_value': 2,
                                  'user_lat': 2.1, 'user_lon': 3.1})
    assert response.status_code == 400


def test_validRequestResponseBody1():
    response = client.get('/api/v1/delivery-order-price',
                          params={'venue_slug': 'home-assignment-venue-helsinki', 'cart_value': 2,
                                  'user_lat': 60.17094, 'user_lon': 24.93087})
    assert response.status_code == 400


def test_validRequestResponseBody2():
    response = client.get('/api/v1/delivery-order-price',
                          params={'venue_slug': 'home-assignment-venue-helsinki', 'cart_value': 2,
                                  'user_lat': 60.17094, 'user_lon': 24.93087})
    assert response.json != None  # noqa: E711


def test_invalidQueryParam1():
    response = client.get('/api/v1/delivery-order-price',
                          params={'venue_slug': 'home-assignment-venue-helsinki', 'cart_value': 2,
                                  'user_lat': 'invalid latitude', 'user_lon': 3.1})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_missingQueryParam():
    response = client.get('/api/v1/delivery-order-price',
                          params={'cart_value': 2, 'user_lat': 2.1, 'user_lon': 3.1})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_emptyQueryParam():
    response = client.get('/api/v1/delivery-order-price',
                          params={'venue_slug': '', 'cart_value': 2, 'user_lat': 2.1, 'user_lon': 3.1})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_invalid_endpoint():
    response = client.get("/api/v1/nonexistent-endpoint")
    assert response.status_code == 404


def test_invalid_http_method():
    response = client.post(
        "/api/v1/delivery-order-price",
        json={"venue_slug": "valid-slug", "cart_value": 100, "user_lat": 60.192059, "user_lon": 24.945831},
    )
    assert response.status_code == 405


def test_invalidQueryParam2():
    response = client.get(
        "/api/v1/delivery-order-price",
        params={"venue_slug": 4, "cart_value": 2, "user_lat": "invalid latitude", "user_lon": 3.1},
    )
    assert response.status_code == 422
    assert "detail" in response.json()
