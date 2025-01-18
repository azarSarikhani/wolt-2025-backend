import pytest
from fastapi.testclient import TestClient

from dopc.app import app


client = TestClient(app)

def test_validRequestResponseSchema():
    response = client.get("/api/v1/delivery-order-price")
    assert response.status_code == 200
    assert response.json().get("delivery_fee") != None  # noqa: E711
