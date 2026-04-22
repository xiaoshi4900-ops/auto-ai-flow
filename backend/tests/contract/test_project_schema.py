import pytest
from app.schemas.project import ProjectCreateRequest, ProjectUpdateRequest, ProjectResponse


def test_project_create_name_required():
    with pytest.raises(Exception):
        ProjectCreateRequest()
    req = ProjectCreateRequest(name="Test")
    assert req.name == "Test"


def test_project_create_description_optional():
    req = ProjectCreateRequest(name="Test")
    assert req.description is None


def test_project_create_with_description():
    req = ProjectCreateRequest(name="Test", description="A test project")
    assert req.description == "A test project"


def test_project_update_all_optional():
    req = ProjectUpdateRequest()
    assert req.name is None
    assert req.description is None


def test_project_response_fields():
    resp = ProjectResponse(id=1, name="Test", owner_id=1)
    dumped = resp.model_dump()
    assert "id" in dumped
    assert "name" in dumped
    assert "owner_id" in dumped
    assert "created_at" in dumped
