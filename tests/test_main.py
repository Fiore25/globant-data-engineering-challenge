import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Globant Data Engineering Challenge API"}

def test_get_hires_per_quarter():
    response = client.get("/report/hires-per-quarter/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_above_average_hires():
    response = client.get("/report/above-average-hires/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0