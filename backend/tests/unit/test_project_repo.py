from app.db.repositories.project_repo import ProjectRepository
from app.db.models.project import Project
from app.db.models.user import User


def _make_user(db):
    user = User(username="owner", email="owner@e.com", hashed_password="h")
    db.add(user)
    db.commit()
    return user


def test_project_create(db):
    user = _make_user(db)
    repo = ProjectRepository(db)
    p = repo.create(name="Test Project", owner_id=user.id, description="desc")
    assert p.id is not None
    assert p.name == "Test Project"
    assert p.owner_id == user.id


def test_project_get_by_id(db):
    user = _make_user(db)
    repo = ProjectRepository(db)
    p = repo.create(name="GetTest", owner_id=user.id)
    found = repo.get_by_id(p.id)
    assert found is not None
    assert found.name == "GetTest"


def test_project_list_by_owner(db):
    user = _make_user(db)
    repo = ProjectRepository(db)
    repo.create(name="P1", owner_id=user.id)
    repo.create(name="P2", owner_id=user.id)
    items, total = repo.list_by_owner(user.id, 1, 20)
    assert total == 2
    assert len(items) == 2


def test_project_update(db):
    user = _make_user(db)
    repo = ProjectRepository(db)
    p = repo.create(name="Old", owner_id=user.id)
    updated = repo.update(p, name="New")
    assert updated.name == "New"


def test_project_soft_delete(db):
    user = _make_user(db)
    repo = ProjectRepository(db)
    p = repo.create(name="ToDelete", owner_id=user.id)
    repo.soft_delete(p)
    assert p.is_deleted is True


def test_project_list_excludes_deleted(db):
    user = _make_user(db)
    repo = ProjectRepository(db)
    p1 = repo.create(name="Active", owner_id=user.id)
    p2 = repo.create(name="Deleted", owner_id=user.id)
    repo.soft_delete(p2)
    items, total = repo.list_by_owner(user.id, 1, 20)
    assert total == 1
    assert items[0].name == "Active"
