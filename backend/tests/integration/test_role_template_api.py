ROUTES = {
    "register": "/api/v1/auth/register",
    "login": "/api/v1/auth/login",
    "role_templates": "/api/v1/role-templates",
    "role_template_detail": "/api/v1/role-templates/{id}",
}


def _extract_data(resp):
    body = resp.json()
    if isinstance(body, dict) and "code" in body and "data" in body:
        return body["data"]
    return body


def _auth_header(client, username="roletemplate_api", email="roletemplate_api@e.com"):
    register_resp = client.post(ROUTES["register"], json={"username": username, "email": email, "password": "123456"})
    assert register_resp.status_code in (200, 201)
    resp = client.post(ROUTES["login"], json={"username": username, "password": "123456"})
    assert resp.status_code == 200
    data = _extract_data(resp)
    return {"Authorization": f"Bearer {data['access_token']}"}


def test_list_role_templates_returns_builtin_items(client):
    headers = _auth_header(client)
    resp = client.get(ROUTES["role_templates"], headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert "items" in data
    keys = {item["key"] for item in data["items"]}
    assert "backend_engineer" in keys
    assert "generic_assistant" in keys


def test_get_role_template_detail_returns_full_fields(client):
    headers = _auth_header(client)
    list_resp = client.get(ROUTES["role_templates"], headers=headers)
    template_id = _extract_data(list_resp)["items"][0]["id"]
    resp = client.get(ROUTES["role_template_detail"].format(id=template_id), headers=headers)
    assert resp.status_code == 200
    data = _extract_data(resp)
    assert "execution_mode" in data
    assert "default_code_policy" in data


def test_get_role_template_not_found_returns_v11_error_code(client):
    headers = _auth_header(client)
    resp = client.get(ROUTES["role_template_detail"].format(id=999999), headers=headers)
    assert resp.status_code == 404
    body = resp.json()
    detail = body.get("data", body).get("detail", body.get("data", body))
    assert detail.get("error_code") == "ROLE_TEMPLATE_NOT_FOUND"


def test_list_role_templates_requires_auth(client):
    resp = client.get(ROUTES["role_templates"])
    assert resp.status_code in (401, 403)
