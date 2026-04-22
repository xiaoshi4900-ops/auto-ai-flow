import pytest
from app.db.models.user import User


def _extract_data(resp):
    body = resp.json()
    if isinstance(body, dict) and "code" in body and "data" in body:
        return body["data"]
    return body


def _auth_header(client, username="projectuser", email="project@e.com"):
    client.post("/api/v1/auth/register", json={"username": username, "email": email, "password": "123456"})
    resp = client.post("/api/v1/auth/login", json={"username": username, "password": "123456"})
    token = _extract_data(resp)["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_project(client):
    headers = _auth_header(client)
    resp = client.post("/api/v1/projects", json={"name": "Demo Project", "description": "demo"}, headers=headers)
    assert resp.status_code in (200, 201)
    data = _extract_data(resp)
    assert "id" in data
    assert data["name"] == "Demo Project"


def test_list_projects(client):
    headers = _auth_header(client)
    client.post("/api/v1/projects", json={"name": "P1"}, headers=headers)
    resp = client.get("/api/v1/projects", headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert "total" in data
    assert data["total"] >= 1


def test_get_project_detail(client):
    headers = _auth_header(client)
    create_resp = client.post("/api/v1/projects", json={"name": "Detail"}, headers=headers)
    pid = _extract_data(create_resp)["id"]
    resp = client.get(f"/api/v1/projects/{pid}", headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert data["name"] == "Detail"


def test_update_project(client):
    headers = _auth_header(client)
    create_resp = client.post("/api/v1/projects", json={"name": "Old"}, headers=headers)
    pid = _extract_data(create_resp)["id"]
    resp = client.put(f"/api/v1/projects/{pid}", json={"name": "New"}, headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert data["name"] == "New"


def test_delete_project(client):
    headers = _auth_header(client)
    create_resp = client.post("/api/v1/projects", json={"name": "ToDelete"}, headers=headers)
    pid = _extract_data(create_resp)["id"]
    resp = client.delete(f"/api/v1/projects/{pid}", headers=headers)
    assert resp.status_code == 200
    resp2 = client.get(f"/api/v1/projects/{pid}", headers=headers)
    assert resp2.status_code == 404


def test_project_unauthorized(client):
    resp = client.get("/api/v1/projects")
    assert resp.status_code == 401
