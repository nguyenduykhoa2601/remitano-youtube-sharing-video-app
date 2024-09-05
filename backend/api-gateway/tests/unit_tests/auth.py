from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_register():
    response = client.post(
        "/register", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}


def test_login():
    response = client.post(
        "/login", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_logout():
    response = client.post(
        "/logout", headers={"Authorization": "Bearer dummy_token"})
    assert response.status_code == 200
    assert response.json() == {"message": "Logged out successfully"}
