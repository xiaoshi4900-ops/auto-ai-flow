from enum import Enum

from pydantic import BaseModel


class ValidationStatusEnum(str, Enum):
    passed = "passed"
    failed = "failed"
    skipped = "skipped"


class ValidationSummarySchema(BaseModel):
    lint: str = "skipped"
    build: str = "skipped"
    unit_tests: str = "skipped"


class CodeHandoffPayload(BaseModel):
    task_goal: str
    changed_files: list[str] = []
    validation_summary: ValidationSummarySchema | dict = ValidationSummarySchema()
    open_issues: list[str] = []
    next_actions: list[str] = []
    artifact_refs: list[str] = []


class CodeTaskResultSchema(BaseModel):
    status: str
    plan_summary: str | None = None
    iterations: list[dict] = []
    code_handoff: CodeHandoffPayload | None = None
    recommend_human_review: bool = False
    open_issues: list[str] = []
