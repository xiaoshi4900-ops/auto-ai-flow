from app.db.models.project import Project
from app.db.models.user import User


def _models():
    import importlib

    role_template_mod = importlib.import_module("app.db.models.role_template")
    code_policy_mod = importlib.import_module("app.db.models.code_policy")
    agent_mod = importlib.import_module("app.db.models.agent")
    return role_template_mod.RoleTemplate, code_policy_mod.CodeExecutionPolicy, agent_mod.Agent


def _setup_project(db):
    user = User(username="v11_model_user", email="v11_model_user@e.com", hashed_password="h")
    db.add(user)
    db.commit()
    project = Project(name="v11-project", owner_id=user.id)
    db.add(project)
    db.commit()
    return project


def test_role_template_and_policy_can_be_created(db):
    RoleTemplate, CodeExecutionPolicy, _ = _models()
    tpl = RoleTemplate(
        key="unit_test_backend_eng",
        name="Unit Test Backend Engineer",
        execution_mode="code_runtime",
        description="Template for backend coding",
    )
    db.add(tpl)
    db.commit()
    policy = CodeExecutionPolicy(
        role_template_id=tpl.id,
        max_iterations=3,
        allow_file_write=False,
        run_lint=True,
        run_build=False,
        run_unit_tests=True,
    )
    db.add(policy)
    db.commit()
    assert tpl.id is not None
    assert policy.id is not None
    assert policy.role_template_id == tpl.id


def test_agent_can_reference_role_template(db):
    RoleTemplate, _, Agent = _models()
    project = _setup_project(db)
    tpl = RoleTemplate(
        key="unit_test_frontend_eng",
        name="Unit Test Frontend Engineer",
        execution_mode="code_runtime",
    )
    db.add(tpl)
    db.commit()
    agent = Agent(
        name="UI Engineer",
        role_name="assistant",
        project_id=project.id,
        role_template_id=tpl.id,
    )
    db.add(agent)
    db.commit()
    assert agent.role_template_id == tpl.id
