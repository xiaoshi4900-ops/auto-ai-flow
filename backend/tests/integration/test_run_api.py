import pytest
from unittest.mock import patch, MagicMock


def _extract_data(resp):
    body = resp.json()
    if isinstance(body, dict) and "code" in body and "data" in body:
        return body["data"]
    return body


def _auth_header(client, username="runapi", email="runapi@e.com"):
    client.post("/api/v1/auth/register", json={"username": username, "email": email, "password": "123456"})
    resp = client.post("/api/v1/auth/login", json={"username": username, "password": "123456"})
    return {"Authorization": f"Bearer {_extract_data(resp)['access_token']}"}


def _create_project_and_workflow(client, headers):
    pid = _extract_data(client.post("/api/v1/projects", json={"name": "RunTest"}, headers=headers))["id"]
    wid = _extract_data(client.post("/api/v1/workflows", json={
        "project_id": pid,
        "name": "RunWF",
        "nodes": [{"node_key": "start_1", "node_type": "start"}, {"node_key": "output_1", "node_type": "output"}],
        "edges": [{"source_node_key": "start_1", "target_node_key": "output_1"}],
    }, headers=headers))["id"]
    return pid, wid


def test_trigger_run(client):
    headers = _auth_header(client)
    pid, wid = _create_project_and_workflow(client, headers)
    with patch("app.tasks.workflow_tasks.execute_workflow") as mock_task:
        mock_task.delay = MagicMock()
        resp = client.post("/api/v1/executions/trigger", json={"workflow_id": wid, "input_payload": {"topic": "test"}}, headers=headers)
    assert resp.status_code in (200, 201)
    data = _extract_data(resp)
    assert "run_id" in data


def test_get_run_status(client):
    headers = _auth_header(client)
    pid, wid = _create_project_and_workflow(client, headers)
    with patch("app.tasks.workflow_tasks.execute_workflow") as mock_task:
        mock_task.delay = MagicMock()
        run_resp = client.post("/api/v1/executions/trigger", json={"workflow_id": wid, "input_payload": {}}, headers=headers)
    run_data = _extract_data(run_resp)
    run_id = run_data.get("run_id")
    if run_id:
        resp = client.get(f"/api/v1/runs/{run_id}", headers=headers)
        assert resp.status_code == 200
        data = _extract_data(resp)
        assert "status" in data["run"]


def test_list_runs(client):
    headers = _auth_header(client)
    pid, wid = _create_project_and_workflow(client, headers)
    resp = client.get(f"/api/v1/runs?workflow_id={wid}", headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert "total" in data


def test_run_not_found(client):
    headers = _auth_header(client)
    resp = client.get("/api/v1/runs/99999", headers=headers)
    assert resp.status_code == 404
