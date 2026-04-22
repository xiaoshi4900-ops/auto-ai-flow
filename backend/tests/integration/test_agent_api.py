import pytest


def _extract_data(resp):
    body = resp.json()
    if isinstance(body, dict) and "code" in body and "data" in body:
        return body["data"]
    return body


def _auth_header(client, username="agentapi", email="agentapi@e.com"):
    client.post("/api/v1/auth/register", json={"username": username, "email": email, "password": "123456"})
    resp = client.post("/api/v1/auth/login", json={"username": username, "password": "123456"})
    data = _extract_data(resp)
    return {"Authorization": f"Bearer {data['access_token']}"}


def _create_project(client, headers):
    resp = client.post("/api/v1/projects", json={"name": "AgentTest"}, headers=headers)
    data = _extract_data(resp)
    return data["id"]


def test_create_agent(client):
    headers = _auth_header(client)
    pid = _create_project(client, headers)
    resp = client.post("/api/v1/agents", json={"name": "Agent1", "project_id": pid, "role_name": "assistant"}, headers=headers)
    assert resp.status_code in (200, 201)
    data = _extract_data(resp)
    assert data["name"] == "Agent1"


def test_list_agents_by_project(client):
    headers = _auth_header(client)
    pid = _create_project(client, headers)
    client.post("/api/v1/agents", json={"name": "A1", "project_id": pid, "role_name": "assistant"}, headers=headers)
    client.post("/api/v1/agents", json={"name": "A2", "project_id": pid, "role_name": "assistant"}, headers=headers)
    resp = client.get(f"/api/v1/agents?project_id={pid}", headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert data["total"] == 2


def test_update_agent(client):
    headers = _auth_header(client)
    pid = _create_project(client, headers)
    create_resp = client.post("/api/v1/agents", json={"name": "Old", "project_id": pid, "role_name": "assistant"}, headers=headers)
    aid = _extract_data(create_resp)["id"]
    resp = client.put(f"/api/v1/agents/{aid}", json={"name": "New"}, headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert data["name"] == "New"


def test_skills_api(client):
    headers = _auth_header(client)
    resp = client.get("/api/v1/skills", headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert "total" in data


def test_tools_api(client):
    headers = _auth_header(client)
    resp = client.get("/api/v1/tools", headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert "total" in data
