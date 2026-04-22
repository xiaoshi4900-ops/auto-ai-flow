ROUTES = {
    "register": "/api/v1/auth/register",
    "login": "/api/v1/auth/login",
    "projects": "/api/v1/projects",
    "role_templates": "/api/v1/role-templates",
    "agents_from_template": "/api/v1/projects/{project_id}/agents/from-template",
}


def _extract_data(resp):
    body = resp.json()
    if isinstance(body, dict) and "code" in body and "data" in body:
        return body["data"]
    return body


def _auth_header(client, username="agtfromtpl", email="agtfromtpl@e.com"):
    register_resp = client.post(ROUTES["register"], json={"username": username, "email": email, "password": "123456"})
    assert register_resp.status_code in (200, 201)
    resp = client.post(ROUTES["login"], json={"username": username, "password": "123456"})
    assert resp.status_code == 200
    data = _extract_data(resp)
    return {"Authorization": f"Bearer {data['access_token']}"}


def _create_project(client, headers, name="TemplateFlow"):
    resp = client.post(ROUTES["projects"], json={"name": name}, headers=headers)
    assert resp.status_code in (200, 201)
    return _extract_data(resp)["id"]


def test_create_agent_from_template_success(client):
    headers = _auth_header(client)
    project_id = _create_project(client, headers)
    list_resp = client.get(ROUTES["role_templates"], headers=headers)
    backend_engineer = next(item for item in _extract_data(list_resp)["items"] if item["key"] == "backend_engineer")
    resp = client.post(
        ROUTES["agents_from_template"].format(project_id=project_id),
        json={"role_template_id": backend_engineer["id"], "name": "Order Service Engineer"},
        headers=headers,
    )
    assert resp.status_code in (200, 201)
    data = _extract_data(resp)
    assert data["name"] == "Order Service Engineer"
    assert data["role_template_id"] == backend_engineer["id"]


def test_create_agent_from_template_allows_field_overrides(client):
    headers = _auth_header(client, username="overrideuser", email="overrideuser@e.com")
    project_id = _create_project(client, headers, name="TemplateOverrides")
    role_templates = _extract_data(client.get(ROUTES["role_templates"], headers=headers))["items"]
    template_id = role_templates[0]["id"]
    resp = client.post(
        ROUTES["agents_from_template"].format(project_id=project_id),
        json={
            "role_template_id": template_id,
            "name": "Custom Name",
            "description": "Custom Description",
            "model_id": 101,
        },
        headers=headers,
    )
    assert resp.status_code in (200, 201)
    data = _extract_data(resp)
    assert data["name"] == "Custom Name"
    assert data["description"] == "Custom Description"
    assert data["model_id"] == 101


def test_create_agent_from_missing_template_returns_404(client):
    headers = _auth_header(client, username="missingtpl", email="missingtpl@e.com")
    project_id = _create_project(client, headers, name="MissingTemplate")
    resp = client.post(
        ROUTES["agents_from_template"].format(project_id=project_id),
        json={"role_template_id": 999999, "name": "Should Fail"},
        headers=headers,
    )
    assert resp.status_code == 404


def test_non_owner_cannot_create_agent_from_template(client):
    owner_headers = _auth_header(client, username="owner11", email="owner11@e.com")
    project_id = _create_project(client, owner_headers, name="OwnerProject")
    role_templates = _extract_data(client.get(ROUTES["role_templates"], headers=owner_headers))["items"]
    template_id = role_templates[0]["id"]

    non_owner_headers = _auth_header(client, username="member11", email="member11@e.com")
    resp = client.post(
        ROUTES["agents_from_template"].format(project_id=project_id),
        json={"role_template_id": template_id, "name": "No Access"},
        headers=non_owner_headers,
    )
    assert resp.status_code in (403, 404)


def test_create_agent_from_template_requires_auth(client):
    resp = client.post(
        ROUTES["agents_from_template"].format(project_id=1),
        json={"role_template_id": 1, "name": "Unauthorized"},
    )
    assert resp.status_code in (401, 403)
