import os
import sys

# Make project root importable (so "import app" works)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_sum_positive_integers():
    response = client.get("/sum", params={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 5.0}


def test_sum_negative_numbers():
    response = client.get("/sum", params={"a": -5, "b": 2})
    assert response.status_code == 200
    assert response.json() == {"result": -3.0}


def test_sum_floats():
    response = client.get("/sum", params={"a": 1.5, "b": 2.25})
    assert response.status_code == 200
    assert response.json()["result"] == 3.75
