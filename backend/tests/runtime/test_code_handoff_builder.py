import importlib


def _handoff_module():
    return importlib.import_module("app.runtime.handoff_builder")


def test_build_code_handoff_collects_changed_files_and_artifacts():
    mod = _handoff_module()
    payload = mod.build_code_handoff(
        task_goal="Refactor service layer",
        iterations=[
            {"changed_files": ["a.py", "b.py"], "artifact_refs": ["artifact://patch-1.diff"]},
            {"changed_files": ["b.py", "c.py"], "artifact_refs": ["artifact://patch-2.diff"]},
        ],
        validation_summary={"lint": "passed", "build": "skipped", "unit_tests": "failed"},
        open_issues=["unit tests failing"],
        next_actions=["fix tests"],
    )
    assert sorted(payload["changed_files"]) == ["a.py", "b.py", "c.py"]
    assert payload["artifact_refs"] == ["artifact://patch-1.diff", "artifact://patch-2.diff"]


def test_build_code_handoff_defaults_missing_validation_to_skipped():
    mod = _handoff_module()
    payload = mod.build_code_handoff(
        task_goal="x",
        iterations=[],
        validation_summary={},
        open_issues=[],
        next_actions=[],
    )
    assert payload["validation_summary"]["lint"] == "skipped"
    assert payload["validation_summary"]["build"] == "skipped"
    assert payload["validation_summary"]["unit_tests"] == "skipped"


def test_build_code_handoff_keeps_open_issues_and_next_actions_serializable():
    mod = _handoff_module()
    payload = mod.build_code_handoff(
        task_goal="x",
        iterations=[],
        validation_summary={"lint": "passed", "build": "passed", "unit_tests": "passed"},
        open_issues=["issue-1"],
        next_actions=["do-1"],
    )
    assert payload["open_issues"] == ["issue-1"]
    assert payload["next_actions"] == ["do-1"]
