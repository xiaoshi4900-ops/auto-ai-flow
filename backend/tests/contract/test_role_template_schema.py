from app.schemas.role_template import (
    ExecutionModeEnum,
    CodeExecutionPolicySchema,
    RoleTemplateListItem,
    RoleTemplateResponse,
    RoleTemplateListResponse,
)


def test_execution_mode_enum_values():
    assert ExecutionModeEnum.normal_llm == "normal_llm"
    assert ExecutionModeEnum.code_runtime == "code_runtime"
    assert ExecutionModeEnum.analysis_runtime == "analysis_runtime"
    assert ExecutionModeEnum.test_runtime == "test_runtime"


def test_code_execution_policy_defaults():
    policy = CodeExecutionPolicySchema()
    assert policy.max_iterations == 3
    assert policy.allow_file_write is False
    assert policy.run_lint is True
    assert policy.run_build is False
    assert policy.run_unit_tests is True
    assert policy.require_plan_first is True
    assert policy.require_integration_tests is False
    assert policy.allow_repo_read is True
    assert policy.allow_repo_write is False
    assert policy.allow_auto_commit is False
    assert policy.allow_auto_pr is False
    assert policy.stop_on_critical_error is True
    assert policy.fallback_to_human is True


def test_role_template_list_item_fields():
    item = RoleTemplateListItem(id=1, key="backend_engineer", name="Backend Engineer", execution_mode="code_runtime")
    data = item.model_dump()
    assert "id" in data
    assert "key" in data
    assert "name" in data
    assert "execution_mode" in data


def test_role_template_response_fields():
    resp = RoleTemplateResponse(
        id=1,
        key="backend_engineer",
        name="Backend Engineer",
        category="engineering",
        description="Writes backend code",
        execution_mode="code_runtime",
        default_role_name="backend_engineer",
        default_model_id=None,
        default_skill_ids=[],
        default_tool_ids=[],
        default_code_policy=None,
        is_builtin=True,
        enabled=True,
    )
    data = resp.model_dump()
    expected_fields = [
        "id", "key", "name", "category", "description", "execution_mode",
        "default_role_name", "default_model_id", "default_skill_ids",
        "default_tool_ids", "default_code_policy", "is_builtin", "enabled",
    ]
    for field in expected_fields:
        assert field in data, f"Missing field: {field}"


def test_role_template_list_response():
    items = [
        RoleTemplateListItem(id=1, key="generic_assistant", name="Generic Assistant", execution_mode="normal_llm"),
        RoleTemplateListItem(id=2, key="backend_engineer", name="Backend Engineer", execution_mode="code_runtime"),
    ]
    resp = RoleTemplateListResponse(items=items)
    assert len(resp.items) == 2
