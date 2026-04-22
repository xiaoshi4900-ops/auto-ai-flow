import importlib


def _resolver_module():
    return importlib.import_module("app.runtime.execution_mode_resolver")


def test_force_execution_mode_has_highest_priority():
    mod = _resolver_module()
    mode = mod.resolve_execution_mode(
        node_config={"force_execution_mode": "analysis_runtime"},
        skill={"execution_mode": "code_runtime"},
        role_template={"execution_mode": "normal_llm"},
    )
    assert mode == "analysis_runtime"


def test_skill_execution_mode_used_when_force_missing():
    mod = _resolver_module()
    mode = mod.resolve_execution_mode(
        node_config={},
        skill={"execution_mode": "code_runtime"},
        role_template={"execution_mode": "normal_llm"},
    )
    assert mode == "code_runtime"


def test_role_template_execution_mode_used_when_skill_missing():
    mod = _resolver_module()
    mode = mod.resolve_execution_mode(node_config={}, skill=None, role_template={"execution_mode": "test_runtime"})
    assert mode == "test_runtime"


def test_default_to_normal_llm_when_all_missing():
    mod = _resolver_module()
    mode = mod.resolve_execution_mode(node_config={}, skill=None, role_template=None)
    assert mode == "normal_llm"
