from unittest.mock import MagicMock


def _runner():
    import importlib

    mod = importlib.import_module("app.runtime.code_skill_runner")
    return mod.CodeSkillRunner()


def test_code_skill_runner_generates_plan_summary_first_iteration():
    runner = _runner()
    result = runner.run(
        workflow_run=MagicMock(id=1),
        workflow_node=MagicMock(node_key="agent_1"),
        runtime_context={"input": {"task": "refactor"}},
        max_iterations=3,
    )
    assert result["plan_summary"]
    assert len(result["iterations"]) >= 1


def test_code_skill_runner_respects_max_iterations():
    runner = _runner()
    result = runner.run(
        workflow_run=MagicMock(id=2),
        workflow_node=MagicMock(node_key="agent_2"),
        runtime_context={"input": {"task": "fix tests"}},
        max_iterations=3,
    )
    assert len(result["iterations"]) <= 3


def test_code_skill_runner_returns_code_task_result_schema_shape():
    runner = _runner()
    result = runner.run(
        workflow_run=MagicMock(id=3),
        workflow_node=MagicMock(node_key="agent_3"),
        runtime_context={"input": {"task": "improve docs"}},
        max_iterations=1,
    )
    assert "status" in result
    assert "iterations" in result
    assert "code_handoff" in result
