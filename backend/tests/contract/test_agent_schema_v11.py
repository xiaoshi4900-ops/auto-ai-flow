import importlib


def _agent_module():
    return importlib.import_module("app.schemas.agent")


def _skill_module():
    return importlib.import_module("app.schemas.skill")


def test_agent_create_accepts_role_template_id():
    mod = _agent_module()
    req = mod.AgentCreateRequest(name="Agent v1.1", project_id=1, role_template_id=2)
    assert req.role_template_id == 2


def test_agent_update_accepts_role_template_id():
    mod = _agent_module()
    req = mod.AgentUpdateRequest(role_template_id=8)
    assert req.role_template_id == 8


def test_agent_response_contains_role_template_id():
    mod = _agent_module()
    resp = mod.AgentResponse(id=1, project_id=1, name="A", role_name="assistant", role_template_id=6)
    assert resp.role_template_id == 6


def test_skill_response_contains_execution_mode():
    mod = _skill_module()
    resp = mod.SkillResponse(
        id=1,
        name="code_writer",
        skill_key="code_writer",
        description="Writes code",
        execution_mode="code_runtime",
    )
    assert resp.execution_mode == "code_runtime"
