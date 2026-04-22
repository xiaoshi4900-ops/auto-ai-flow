from app.schemas.code_runtime import (
    ValidationStatusEnum,
    ValidationSummarySchema,
    CodeHandoffPayload,
    CodeTaskResultSchema,
)


def test_validation_status_enum():
    assert ValidationStatusEnum.passed == "passed"
    assert ValidationStatusEnum.failed == "failed"
    assert ValidationStatusEnum.skipped == "skipped"


def test_validation_summary_defaults():
    vs = ValidationSummarySchema()
    assert vs.lint == "skipped"
    assert vs.build == "skipped"
    assert vs.unit_tests == "skipped"


def test_code_handoff_payload_fields():
    payload = CodeHandoffPayload(
        task_goal="Implement feature X",
        changed_files=["app/main.py", "app/utils.py"],
        validation_summary=ValidationSummarySchema(lint="passed", build="skipped", unit_tests="passed"),
        open_issues=[],
        next_actions=["Verify in staging"],
        artifact_refs=["artifact://patch-1.diff"],
    )
    data = payload.model_dump()
    assert data["task_goal"] == "Implement feature X"
    assert len(data["changed_files"]) == 2
    assert data["validation_summary"]["lint"] == "passed"
    assert len(data["artifact_refs"]) == 1


def test_code_task_result_schema():
    result = CodeTaskResultSchema(
        status="success",
        plan_summary="Plan: implement feature",
        iterations=[{"iteration_no": 1, "status": "completed"}],
        code_handoff=CodeHandoffPayload(
            task_goal="Implement feature X",
            changed_files=["app/main.py"],
            validation_summary=ValidationSummarySchema(lint="passed"),
        ),
        recommend_human_review=False,
        open_issues=[],
    )
    data = result.model_dump()
    assert data["status"] == "success"
    assert len(data["iterations"]) == 1
    assert data["code_handoff"]["task_goal"] == "Implement feature X"
