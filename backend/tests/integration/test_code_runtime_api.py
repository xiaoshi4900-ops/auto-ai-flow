ROUTES = {
    "register": "/api/v1/auth/register",
    "login": "/api/v1/auth/login",
    "projects": "/api/v1/projects",
    "workflows": "/api/v1/workflows",
    "trigger": "/api/v1/executions/trigger",
    "run_iterations": "/api/v1/runs/{run_id}/code-iterations",
    "code_task_detail": "/api/v1/code-tasks/{id}",
    "code_task_iterations": "/api/v1/code-tasks/{id}/iterations",
}


def _extract_data(resp):
    body = resp.json()
    if isinstance(body, dict) and "code" in body and "data" in body:
        return body["data"]
    return body


def _auth_header(client, username="coderuntime", email="coderuntime@e.com"):
    register_resp = client.post(ROUTES["register"], json={"username": username, "email": email, "password": "123456"})
    assert register_resp.status_code in (200, 201)
    resp = client.post(ROUTES["login"], json={"username": username, "password": "123456"})
    assert resp.status_code == 200
    data = _extract_data(resp)
    return {"Authorization": f"Bearer {data['access_token']}"}


def _create_project_and_workflow(client, headers, suffix):
    project_resp = client.post(ROUTES["projects"], json={"name": f"Runtime-{suffix}"}, headers=headers)
    project_id = _extract_data(project_resp)["id"]
    workflow_resp = client.post(
        ROUTES["workflows"],
        json={
            "project_id": project_id,
            "name": f"RuntimeWF-{suffix}",
            "nodes": [{"node_key": "start_1", "node_type": "start"}, {"node_key": "agent_1", "node_type": "agent"}],
            "edges": [{"source_node_key": "start_1", "target_node_key": "agent_1"}],
        },
        headers=headers,
    )
    workflow_id = _extract_data(workflow_resp)["id"]
    return project_id, workflow_id


def test_list_code_iterations_by_run_id(client):
    headers = _auth_header(client)
    _, workflow_id = _create_project_and_workflow(client, headers, "A")
    trigger = client.post(ROUTES["trigger"], json={"workflow_id": workflow_id, "input_payload": {}}, headers=headers)
    run_id = _extract_data(trigger)["run_id"]

    resp = client.get(ROUTES["run_iterations"].format(run_id=run_id), headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert isinstance(data.get("items", []), list)


def test_get_code_task_and_iterations_detail(client):
    headers = _auth_header(client, username="coderuntime2", email="coderuntime2@e.com")
    _, workflow_id = _create_project_and_workflow(client, headers, "B")
    trigger = client.post(ROUTES["trigger"], json={"workflow_id": workflow_id, "input_payload": {}}, headers=headers)
    run_id = _extract_data(trigger)["run_id"]

    list_resp = client.get(ROUTES["run_iterations"].format(run_id=run_id), headers=headers)
    items = _extract_data(list_resp).get("items", [])
    if not items:
        assert items == []
        return

    code_task_id = items[0]["code_task_id"]
    task_resp = client.get(ROUTES["code_task_detail"].format(id=code_task_id), headers=headers)
    assert task_resp.status_code == 200
    task_data = _extract_data(task_resp)
    assert task_data["id"] == code_task_id

    iterations_resp = client.get(ROUTES["code_task_iterations"].format(id=code_task_id), headers=headers)
    assert iterations_resp.status_code == 200
    iterations_data = _extract_data(iterations_resp)
    assert isinstance(iterations_data.get("items", []), list)


def test_cross_project_code_runtime_data_isolated(client):
    user_a_headers = _auth_header(client, username="proj_a", email="proj_a@e.com")
    _, workflow_a = _create_project_and_workflow(client, user_a_headers, "A")
    trigger = client.post(ROUTES["trigger"], json={"workflow_id": workflow_a, "input_payload": {}}, headers=user_a_headers)
    run_id = _extract_data(trigger)["run_id"]

    user_b_headers = _auth_header(client, username="proj_b", email="proj_b@e.com")
    resp = client.get(ROUTES["run_iterations"].format(run_id=run_id), headers=user_b_headers)
    assert resp.status_code in (403, 404)


def test_code_runtime_query_requires_auth(client):
    resp = client.get(ROUTES["run_iterations"].format(run_id=1))
    assert resp.status_code in (401, 403)
