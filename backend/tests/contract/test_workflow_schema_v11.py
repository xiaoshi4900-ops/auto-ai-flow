import importlib


def _workflow_module():
    return importlib.import_module("app.schemas.workflow")


def test_agent_node_config_accepts_force_execution_mode():
    mod = _workflow_module()
    cfg = mod.AgentNodeConfigSchema(
        agent_id=1,
        task_instruction="Do coding task",
        force_execution_mode="code_runtime",
    )
    assert cfg.force_execution_mode == "code_runtime"


def test_agent_node_config_accepts_code_policy_override():
    mod = _workflow_module()
    cfg = mod.AgentNodeConfigSchema(
        agent_id=1,
        code_policy_override={
            "max_iterations": 2,
            "allow_file_write": False,
            "run_lint": True,
            "run_build": False,
            "run_unit_tests": True,
        },
    )
    assert cfg.code_policy_override["max_iterations"] == 2


def test_agent_node_config_accepts_workspace_binding():
    mod = _workflow_module()
    cfg = mod.AgentNodeConfigSchema(
        agent_id=1,
        workspace_binding={"workspace_id": "ws_default", "repo_path": "/tmp/repo"},
    )
    assert cfg.workspace_binding["workspace_id"] == "ws_default"
