from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_sum_ok():
    response = client.get("/calc/sum?a=2&b=3")
    assert response.status_code == 200
    assert response.json() == {"result": 5}


def test_sum_missing_params():
    response = client.get("/calc/sum?a=2")
    assert response.status_code == 400
    assert response.json()["detail"] == "Both 'a' and 'b' query params are required"
