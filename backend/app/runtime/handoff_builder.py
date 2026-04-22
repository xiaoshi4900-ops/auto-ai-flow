from app.schemas.runtime import HandoffPayloadSchema


class HandoffBuilder:
    def build(self, node_type: str, raw_output: dict, structured_output: dict) -> HandoffPayloadSchema:
        summary = ""
        if isinstance(raw_output, dict):
            summary = str(raw_output.get("summary", raw_output.get("result", "")))[:500]
        elif isinstance(raw_output, str):
            summary = raw_output[:500]

        assumptions = []
        risks = []
        questions = []

        if isinstance(raw_output, dict):
            assumptions = raw_output.get("assumptions", [])
            risks = raw_output.get("risks", [])
            questions = raw_output.get("questions_for_next_node", [])

        return HandoffPayloadSchema(
            handoff_summary=summary,
            assumptions=assumptions if isinstance(assumptions, list) else [],
            risks=risks if isinstance(risks, list) else [],
            questions_for_next_node=questions if isinstance(questions, list) else [],
        )


def build_code_handoff(task_goal: str, iterations: list, validation_summary: dict, open_issues: list, next_actions: list) -> dict:
    all_changed = []
    all_artifacts = []
    for it in iterations:
        for f in it.get("changed_files", []):
            if f not in all_changed:
                all_changed.append(f)
        for a in it.get("artifact_refs", []):
            all_artifacts.append(a)

    lint = validation_summary.get("lint", "skipped")
    build = validation_summary.get("build", "skipped")
    unit_tests = validation_summary.get("unit_tests", "skipped")

    return {
        "task_goal": task_goal,
        "changed_files": all_changed,
        "validation_summary": {
            "lint": lint,
            "build": build,
            "unit_tests": unit_tests,
        },
        "open_issues": open_issues or [],
        "next_actions": next_actions or [],
        "artifact_refs": all_artifacts,
    }
