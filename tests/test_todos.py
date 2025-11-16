from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get():
    r = client.post("/todos", json={"title": "learn fastapi"})
    assert r.status_code == 201
    todo = r.json()
    assert todo["title"] == "learn fastapi"
    tid = todo["id"]

    r = client.get(f"/todos/{tid}")
    assert r.status_code == 200
    assert r.json()["id"] == tid

def test_list_and_update_and_delete():
    client.post("/todos", json={"title": "a"})
    client.post("/todos", json={"title": "b", "done": True})

    r = client.get("/todos")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 2

    tid = items[-1]["id"]
    r = client.patch(f"/todos/{tid}", json={"done": False, "title": "b2"})
    assert r.status_code == 200
    body = r.json()
    assert body["done"] is False and body["title"] == "b2"

    r = client.delete(f"/todos/{tid}")
    assert r.status_code == 204

    r = client.get(f"/todos/{tid}")
    assert r.status_code == 404

def test_validation():
    r = client.post("/todos", json={"title": ""})
    assert r.status_code == 422
