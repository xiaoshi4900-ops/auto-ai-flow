from enum import Enum

from pydantic import BaseModel


class ExecutionModeEnum(str, Enum):
    normal_llm = "normal_llm"
    code_runtime = "code_runtime"
    analysis_runtime = "analysis_runtime"
    test_runtime = "test_runtime"


class CodeExecutionPolicySchema(BaseModel):
    max_iterations: int = 3
    allow_file_write: bool = False
    run_lint: bool = True
    run_build: bool = False
    run_unit_tests: bool = True
    require_plan_first: bool = True
    require_integration_tests: bool = False
    allow_repo_read: bool = True
    allow_repo_write: bool = False
    allow_auto_commit: bool = False
    allow_auto_pr: bool = False
    stop_on_critical_error: bool = True
    fallback_to_human: bool = True


class RoleTemplateListItem(BaseModel):
    id: int
    key: str
    name: str
    execution_mode: ExecutionModeEnum

    model_config = {"from_attributes": True}


class RoleTemplateResponse(BaseModel):
    id: int
    key: str
    name: str
    category: str | None = None
    description: str | None = None
    execution_mode: ExecutionModeEnum
    default_role_name: str | None = None
    default_model_id: int | None = None
    default_skill_ids: list[int] = []
    default_tool_ids: list[int] = []
    default_code_policy: CodeExecutionPolicySchema | None = None
    is_builtin: bool = False
    enabled: bool = True

    model_config = {"from_attributes": True}


class RoleTemplateListResponse(BaseModel):
    items: list[RoleTemplateListItem]
