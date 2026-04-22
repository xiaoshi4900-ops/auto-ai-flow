import pytest
from unittest.mock import MagicMock, patch
from app.services.project_service import ProjectService
from app.core.exceptions import NotFoundException, ForbiddenException
from app.schemas.project import ProjectCreateRequest, ProjectUpdateRequest
from app.db.models.project import Project


def _make_project(id=1, name="Test", owner_id=1):
    p = Project(name=name, owner_id=owner_id)
    p.id = id
    return p


def test_project_create(db):
    service = ProjectService(db)
    with patch.object(service.repo, "create", return_value=_make_project()):
        req = ProjectCreateRequest(name="Test")
        result = service.create(req, owner_id=1)
    assert result.name == "Test"


def test_project_get_owner(db):
    service = ProjectService(db)
    with patch.object(service.repo, "get_by_id", return_value=_make_project(owner_id=1)):
        result = service.get(1, user_id=1)
    assert result.name == "Test"


def test_project_get_not_owner(db):
    service = ProjectService(db)
    with patch.object(service.repo, "get_by_id", return_value=_make_project(owner_id=1)):
        with pytest.raises(ForbiddenException):
            service.get(1, user_id=2)


def test_project_get_not_found(db):
    service = ProjectService(db)
    with patch.object(service.repo, "get_by_id", return_value=None):
        with pytest.raises(NotFoundException):
            service.get(999, user_id=1)


def test_project_delete_not_found(db):
    service = ProjectService(db)
    with patch.object(service.repo, "get_by_id", return_value=None):
        with pytest.raises(NotFoundException):
            service.delete(999, user_id=1)


def test_project_update_success(db):
    service = ProjectService(db)
    project = _make_project(owner_id=1)
    updated = _make_project(name="Updated")
    with patch.object(service.repo, "get_by_id", return_value=project):
        with patch.object(service.repo, "update", return_value=updated):
            req = ProjectUpdateRequest(name="Updated")
            result = service.update(1, req, user_id=1)
    assert result.name == "Updated"
