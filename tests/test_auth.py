from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup_and_login_and_me():
    # 1) signup
    email = "user1@example.com"
    password = "secret123"

    r = client.post("/users/signup", json={"email": email, "password": password})
    assert r.status_code == 201
    user = r.json()
    assert user["email"] == email
    assert "id" in user
    assert user["is_active"] is True

    # 2) login
    r = client.post(
        "/auth/token",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200
    token_data = r.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    access_token = token_data["access_token"]

    # 3) access protected endpoint
    r = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert r.status_code == 200
    me = r.json()
    assert me["email"] == email
    assert me["id"] == user["id"]
