import pytest
from app.db.models.role_template import RoleTemplate
from app.db.models.code_task import CodeTask
from app.db.models.code_iteration import CodeIteration
from app.db.models.code_policy import CodeExecutionPolicy
from app.db.models.code_workspace import CodeWorkspace


def _extract_data(resp):
    if hasattr(resp, "json"):
        body = resp.json()
        if isinstance(body, dict) and "data" in body:
            return body["data"]
        return body
    return resp


def _auth_header(client, username="v11test", email="v11test@e.com"):
    client.post("/api/v1/auth/register", json={"username": username, "email": email, "password": "123456"})
    resp = client.post("/api/v1/auth/login", json={"username": username, "password": "123456"})
    data = _extract_data(resp)
    return {"Authorization": f"Bearer {data['access_token']}"}


class TestRoleTemplateAPI:
    def test_list_role_templates(self, client):
        headers = _auth_header(client)
        resp = client.get("/api/v1/role-templates", headers=headers)
        assert resp.status_code == 200
        data = _extract_data(resp)
        assert "items" in data
        assert len(data["items"]) >= 1

    def test_get_role_template_detail(self, client, db):
        headers = _auth_header(client)
        tpl = db.query(RoleTemplate).first()
        assert tpl is not None
        resp = client.get(f"/api/v1/role-templates/{tpl.id}", headers=headers)
        assert resp.status_code == 200
        data = _extract_data(resp)
        assert data["key"] == tpl.key
        assert data["name"] == tpl.name
        assert "execution_mode" in data
        assert "is_builtin" in data
        assert "enabled" in data

    def test_get_role_template_not_found(self, client):
        headers = _auth_header(client)
        resp = client.get("/api/v1/role-templates/99999", headers=headers)
        assert resp.status_code == 404

    def test_builtin_templates_seeded(self, client):
        headers = _auth_header(client)
        resp = client.get("/api/v1/role-templates", headers=headers)
        data = _extract_data(resp)
        keys = [t["key"] for t in data["items"]]
        assert "generic_assistant" in keys
        assert "backend_engineer" in keys
        assert "frontend_engineer" in keys

    def test_code_runtime_template_has_policy(self, client, db):
        headers = _auth_header(client)
        tpl = db.query(RoleTemplate).filter(RoleTemplate.execution_mode == "code_runtime").first()
        assert tpl is not None
        resp = client.get(f"/api/v1/role-templates/{tpl.id}", headers=headers)
        data = _extract_data(resp)
        assert data["default_code_policy"] is not None
        assert data["default_code_policy"]["max_iterations"] > 0


class TestAgentFromTemplate:
    def test_create_agent_from_template(self, client, db):
        from app.db.models.project import Project
        from app.db.models.user import User
        headers = _auth_header(client)
        user = db.query(User).first()
        project = Project(name="Test Project", owner_id=user.id)
        db.add(project)
        db.commit()

        tpl = db.query(RoleTemplate).filter(RoleTemplate.key == "backend_engineer").first()
        assert tpl is not None

        resp = client.post(
            f"/api/v1/projects/{project.id}/agents/from-template",
            json={"role_template_id": tpl.id, "name": "My Backend Agent"},
            headers=headers,
        )
        assert resp.status_code == 200
        data = _extract_data(resp)
        assert data["name"] == "My Backend Agent"
        assert data["role_template_id"] == tpl.id
        assert data["role_name"] == tpl.default_role_name

    def test_create_agent_from_template_not_found(self, client, db):
        from app.db.models.project import Project
        from app.db.models.user import User
        headers = _auth_header(client)
        user = db.query(User).first()
        project = Project(name="Test Project 2", owner_id=user.id)
        db.add(project)
        db.commit()

        resp = client.post(
            f"/api/v1/projects/{project.id}/agents/from-template",
            json={"role_template_id": 99999},
            headers=headers,
        )
        assert resp.status_code == 404

    def test_create_agent_from_template_uses_defaults(self, client, db):
        from app.db.models.project import Project
        from app.db.models.user import User
        headers = _auth_header(client)
        user = db.query(User).first()
        project = Project(name="Test Project 3", owner_id=user.id)
        db.add(project)
        db.commit()

        tpl = db.query(RoleTemplate).filter(RoleTemplate.key == "generic_assistant").first()
        resp = client.post(
            f"/api/v1/projects/{project.id}/agents/from-template",
            json={"role_template_id": tpl.id},
            headers=headers,
        )
        assert resp.status_code == 200
        data = _extract_data(resp)
        assert data["name"] == tpl.name
        assert data["role_template_id"] == tpl.id


class TestCodeRuntimeAPI:
    def test_list_code_iterations_by_run(self, client, db):
        from app.db.models.user import User
        from app.db.models.project import Project
        from app.db.models.workflow import Workflow
        from app.db.models.run import WorkflowRun
        headers = _auth_header(client)

        user = db.query(User).first()
        project = Project(name="Code Runtime Project", owner_id=user.id)
        db.add(project)
        db.commit()

        workflow = Workflow(name="Code Workflow", project_id=project.id, canvas_data={})
        db.add(workflow)
        db.commit()

        run = WorkflowRun(workflow_id=workflow.id, status="running")
        db.add(run)
        db.commit()

        task = CodeTask(workflow_run_id=run.id, task_goal="Implement feature", status="running")
        db.add(task)
        db.commit()

        iter1 = CodeIteration(code_task_id=task.id, iteration_no=1, status="completed", validation_lint="passed", validation_unit_tests="passed")
        iter2 = CodeIteration(code_task_id=task.id, iteration_no=2, status="completed", validation_lint="passed", validation_unit_tests="passed")
        db.add_all([iter1, iter2])
        db.commit()

        resp = client.get(f"/api/v1/runs/{run.id}/code-iterations", headers=headers)
        assert resp.status_code == 200
        data = _extract_data(resp)
        assert "items" in data
        assert len(data["items"]) == 2

    def test_get_code_task(self, client, db):
        from app.db.models.user import User
        from app.db.models.project import Project
        from app.db.models.workflow import Workflow
        from app.db.models.run import WorkflowRun
        headers = _auth_header(client)

        user = db.query(User).first()
        project = Project(name="Code Task Project", owner_id=user.id)
        db.add(project)
        db.commit()

        workflow = Workflow(name="Code Task Workflow", project_id=project.id, canvas_data={})
        db.add(workflow)
        db.commit()

        run = WorkflowRun(workflow_id=workflow.id, status="running")
        db.add(run)
        db.commit()

        task = CodeTask(workflow_run_id=run.id, task_goal="Write tests", status="running")
        db.add(task)
        db.commit()

        resp = client.get(f"/api/v1/code-tasks/{task.id}", headers=headers)
        assert resp.status_code == 200
        data = _extract_data(resp)
        assert data["task_goal"] == "Write tests"

    def test_code_task_not_found(self, client):
        headers = _auth_header(client)
        resp = client.get("/api/v1/code-tasks/99999", headers=headers)
        assert resp.status_code == 404


class TestExecutionModeResolver:
    def test_force_execution_mode(self):
        from app.runtime.execution_mode_resolver import resolve_execution_mode
        config = {"force_execution_mode": "code_runtime"}
        assert resolve_execution_mode(config) == "code_runtime"

    def test_skill_execution_mode(self):
        from app.runtime.execution_mode_resolver import resolve_execution_mode
        config = {}
        skill = {"execution_mode": "code_runtime"}
        assert resolve_execution_mode(config, skill=skill) == "code_runtime"

    def test_role_template_execution_mode(self):
        from app.runtime.execution_mode_resolver import resolve_execution_mode
        config = {}
        tpl = {"execution_mode": "analysis_runtime"}
        assert resolve_execution_mode(config, role_template=tpl) == "analysis_runtime"

    def test_default_normal_llm(self):
        from app.runtime.execution_mode_resolver import resolve_execution_mode
        assert resolve_execution_mode({}) == "normal_llm"

    def test_force_overrides_skill(self):
        from app.runtime.execution_mode_resolver import resolve_execution_mode
        config = {"force_execution_mode": "normal_llm"}
        skill = {"execution_mode": "code_runtime"}
        assert resolve_execution_mode(config, skill=skill) == "normal_llm"


class TestCodeSkillRunner:
    def test_code_skill_runner_success(self):
        from app.runtime.code_skill_runner import CodeSkillRunner
        runner = CodeSkillRunner()
        result = runner.run(
            workflow_run=None,
            workflow_node=None,
            runtime_context={"input": {"task": "Write a function"}},
            max_iterations=2,
        )
        assert result["status"] == "success"
        assert len(result["iterations"]) == 2
        assert result["code_handoff"] is not None
        assert result["recommend_human_review"] is False

    def test_code_skill_runner_failure(self):
        from app.runtime.code_skill_runner import CodeSkillRunner
        runner = CodeSkillRunner()
        result = runner.run(
            workflow_run=None,
            workflow_node=None,
            runtime_context={"input": {"task": "Write a function"}},
            max_iterations=3,
            force_fail=True,
        )
        assert result["status"] == "failed"
        assert result["recommend_human_review"] is True
        assert len(result["open_issues"]) > 0

    def test_code_skill_runner_handoff_structure(self):
        from app.runtime.code_skill_runner import CodeSkillRunner
        runner = CodeSkillRunner()
        result = runner.run(
            workflow_run=None,
            workflow_node=None,
            runtime_context={"input": {"task": "Write a function"}},
            max_iterations=1,
        )
        handoff = result["code_handoff"]
        assert "task_goal" in handoff
        assert "changed_files" in handoff
        assert "validation_summary" in handoff
        assert "open_issues" in handoff
        assert "next_actions" in handoff
        assert "artifact_refs" in handoff
