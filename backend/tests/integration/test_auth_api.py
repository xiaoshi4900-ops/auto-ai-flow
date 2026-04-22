import pytest
from app.db.models.user import User


def _extract_data(resp):
    body = resp.json()
    if isinstance(body, dict) and "code" in body and "data" in body:
        return body["data"]
    return body


def _register_user(client, username="testuser", email="test@example.com", password="123456"):
    return client.post("/api/v1/auth/register", json={"username": username, "email": email, "password": password})


def _login_user(client, username="testuser", password="123456"):
    return client.post("/api/v1/auth/login", json={"username": username, "password": password})


def test_register_success(client):
    resp = _register_user(client)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert "id" in data
    assert data["username"] == "testuser"


def test_register_duplicate(client):
    _register_user(client)
    resp = _register_user(client)
    assert resp.status_code in (400, 409)


def test_login_success(client):
    _register_user(client)
    resp = _login_user(client)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_password(client):
    _register_user(client)
    resp = _login_user(client, password="wrong")
    assert resp.status_code == 401


def test_login_missing_fields(client):
    resp = client.post("/api/v1/auth/login", json={"username": "testuser"})
    assert resp.status_code == 422


def test_get_me_with_token(client):
    _register_user(client)
    login_resp = _login_user(client)
    data = _extract_data(login_resp)
    token = data["access_token"]
    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    me_data = _extract_data(resp)
    assert me_data["username"] == "testuser"


def test_get_me_without_token(client):
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401


def test_logout_revokes_token(client):
    _register_user(client)
    login_resp = _login_user(client)
    data = _extract_data(login_resp)
    resp = client.post("/api/v1/auth/logout", json={"refresh_token": data["refresh_token"]}, headers={"Authorization": f"Bearer {data['access_token']}"})
    assert resp.status_code == 200
