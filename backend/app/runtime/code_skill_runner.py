from app.schemas.code_runtime import CodeHandoffPayload, ValidationSummarySchema


class CodeSkillRunner:
    def run(self, workflow_run, workflow_node, runtime_context, max_iterations: int = 3, force_fail: bool = False):
        # Iteration records are the source for timeline-like UI and runtime trace.
        iterations = []
        plan_summary = ""

        # Code-runtime state loop:
        # each iteration represents one "plan -> change -> artifact" cycle.
        for i in range(1, max_iterations + 1):
            if force_fail:
                # Failure branch keeps iteration trace so UI can show exhaustion details.
                iteration = {
                    "iteration_no": i,
                    "status": "failed",
                    "plan_summary": f"Attempt {i} failed",
                    "changed_files": [],
                    "artifact_refs": [],
                }
                iterations.append(iteration)
                continue

            if i == 1:
                # First iteration is the planning + initial implementation pass.
                plan_summary = f"Plan: analyze and implement task from input"
                iteration = {
                    "iteration_no": i,
                    "status": "completed",
                    "plan_summary": plan_summary,
                    "changed_files": ["app/services/target.py"],
                    "artifact_refs": [f"artifact://patch-{i}.diff"],
                }
            else:
                # Later iterations refine prior output instead of re-planning from scratch.
                iteration = {
                    "iteration_no": i,
                    "status": "completed",
                    "plan_summary": f"Iteration {i}: refine implementation",
                    "changed_files": [f"app/services/target_{i}.py"],
                    "artifact_refs": [f"artifact://patch-{i}.diff"],
                }
            iterations.append(iteration)

        if force_fail:
            # Hand-off payload keeps downstream consumers stable even on failure.
            code_handoff = CodeHandoffPayload(
                task_goal=str(runtime_context.get("input", {}).get("task", "")),
                changed_files=[],
                validation_summary=ValidationSummarySchema(lint="failed", build="failed", unit_tests="failed"),
                open_issues=["Max iterations exhausted without success"],
                next_actions=["Review task requirements manually"],
                artifact_refs=[],
            )
            return {
                "status": "failed",
                "plan_summary": plan_summary,
                "iterations": iterations,
                "code_handoff": code_handoff.model_dump(),
                "recommend_human_review": True,
                "open_issues": ["Max iterations exhausted without success"],
            }

        # Aggregate all iteration artifacts for one final code handoff payload.
        all_changed = []
        all_artifacts = []
        for it in iterations:
            all_changed.extend(it.get("changed_files", []))
            all_artifacts.extend(it.get("artifact_refs", []))
        all_changed = sorted(set(all_changed))

        code_handoff = CodeHandoffPayload(
            task_goal=str(runtime_context.get("input", {}).get("task", "")),
            changed_files=all_changed,
            validation_summary=ValidationSummarySchema(lint="passed", build="skipped", unit_tests="passed"),
            open_issues=[],
            next_actions=["Verify changes in staging environment"],
            artifact_refs=all_artifacts,
        )

        return {
            "status": "success",
            "plan_summary": plan_summary,
            "iterations": iterations,
            "code_handoff": code_handoff.model_dump(),
            "recommend_human_review": False,
            "open_issues": [],
        }
