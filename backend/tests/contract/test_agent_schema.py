import pytest
from app.schemas.agent import AgentCreateRequest, AgentUpdateRequest, AgentResponse


def test_agent_create_required_fields():
    with pytest.raises(Exception):
        AgentCreateRequest()
    req = AgentCreateRequest(name="Agent1", project_id=1)
    assert req.name == "Agent1"
    assert req.role_name == "assistant"


def test_agent_create_optional_fields():
    req = AgentCreateRequest(name="Agent1", project_id=1, skill_ids=[1, 2], tool_ids=[3])
    assert req.skill_ids == [1, 2]
    assert req.tool_ids == [3]


def test_agent_update_all_optional():
    req = AgentUpdateRequest()
    assert req.name is None
    assert req.model_id is None


def test_agent_response_no_hashed_password():
    resp = AgentResponse(id=1, project_id=1, name="A", role_name="assistant")
    dumped = resp.model_dump()
    assert "hashed_password" not in dumped
    assert "password" not in dumped


def test_agent_response_skill_tool_ids():
    resp = AgentResponse(id=1, project_id=1, name="A", role_name="assistant", skill_ids=[1], tool_ids=[2])
    assert resp.skill_ids == [1]
    assert resp.tool_ids == [2]
