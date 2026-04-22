from unittest.mock import MagicMock


def _runner():
    import importlib

    mod = importlib.import_module("app.runtime.code_skill_runner")
    return mod.CodeSkillRunner()


def test_code_skill_runner_returns_failed_when_max_iterations_exhausted():
    runner = _runner()
    result = runner.run(
        workflow_run=MagicMock(id=10),
        workflow_node=MagicMock(node_key="agent_failure"),
        runtime_context={"input": {"task": "force_failure"}},
        max_iterations=1,
        force_fail=True,
    )
    assert result["status"] == "failed"
    assert result["recommend_human_review"] is True
    assert result["open_issues"]
