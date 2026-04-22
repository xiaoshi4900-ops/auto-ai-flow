import pytest


def _extract_data(resp):
    body = resp.json()
    if isinstance(body, dict) and "code" in body and "data" in body:
        return body["data"]
    return body


def _auth_header(client, username="wfapi", email="wfapi@e.com"):
    client.post("/api/v1/auth/register", json={"username": username, "email": email, "password": "123456"})
    resp = client.post("/api/v1/auth/login", json={"username": username, "password": "123456"})
    return {"Authorization": f"Bearer {_extract_data(resp)['access_token']}"}


def _create_project(client, headers):
    resp = client.post("/api/v1/projects", json={"name": "WFTest"}, headers=headers)
    return _extract_data(resp)["id"]


def test_create_workflow(client):
    headers = _auth_header(client)
    pid = _create_project(client, headers)
    resp = client.post("/api/v1/workflows", json={
        "project_id": pid,
        "name": "TestWF",
        "nodes": [{"node_key": "start_1", "node_type": "start"}, {"node_key": "output_1", "node_type": "output"}],
        "edges": [{"source_node_key": "start_1", "target_node_key": "output_1"}],
    }, headers=headers)
    assert resp.status_code in (200, 201)
    data = _extract_data(resp)
    assert data["name"] == "TestWF"


def test_list_workflows(client):
    headers = _auth_header(client)
    pid = _create_project(client, headers)
    client.post("/api/v1/workflows", json={"project_id": pid, "name": "WF1"}, headers=headers)
    resp = client.get(f"/api/v1/workflows?project_id={pid}", headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert data["total"] >= 1


def test_get_workflow(client):
    headers = _auth_header(client)
    pid = _create_project(client, headers)
    create_resp = client.post("/api/v1/workflows", json={"project_id": pid, "name": "DetailWF"}, headers=headers)
    wid = _extract_data(create_resp)["id"]
    resp = client.get(f"/api/v1/workflows/{wid}", headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert data["name"] == "DetailWF"


def test_update_workflow(client):
    headers = _auth_header(client)
    pid = _create_project(client, headers)
    create_resp = client.post("/api/v1/workflows", json={"project_id": pid, "name": "OldWF"}, headers=headers)
    wid = _extract_data(create_resp)["id"]
    resp = client.put(f"/api/v1/workflows/{wid}", json={"name": "NewWF"}, headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert data["name"] == "NewWF"


def test_delete_workflow(client):
    headers = _auth_header(client)
    pid = _create_project(client, headers)
    create_resp = client.post("/api/v1/workflows", json={"project_id": pid, "name": "DelWF"}, headers=headers)
    wid = _extract_data(create_resp)["id"]
    resp = client.delete(f"/api/v1/workflows/{wid}", headers=headers)
    assert resp.status_code == 200
    resp2 = client.get(f"/api/v1/workflows/{wid}", headers=headers)
    assert resp2.status_code == 404
