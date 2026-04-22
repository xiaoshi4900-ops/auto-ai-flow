from app.runtime.handoff_builder import HandoffBuilder


def test_build_with_dict_output():
    builder = HandoffBuilder()
    result = builder.build("agent", {"summary": "test result", "result": "ok"}, {})
    assert result.handoff_summary == "test result"
    assert result.assumptions == []
    assert result.risks == []
    assert result.questions_for_next_node == []


def test_build_with_string_output():
    builder = HandoffBuilder()
    result = builder.build("agent", "plain text output", {})
    assert result.handoff_summary == "plain text output"


def test_build_with_assumptions():
    builder = HandoffBuilder()
    raw = {"summary": "s", "assumptions": ["a1", "a2"], "risks": ["r1"], "questions_for_next_node": ["q1"]}
    result = builder.build("agent", raw, {})
    assert result.assumptions == ["a1", "a2"]
    assert result.risks == ["r1"]
    assert result.questions_for_next_node == ["q1"]


def test_build_null_fields_return_empty_list():
    builder = HandoffBuilder()
    raw = {"summary": "s", "assumptions": None, "risks": None, "questions_for_next_node": None}
    result = builder.build("agent", raw, {})
    assert result.assumptions == []
    assert result.risks == []
    assert result.questions_for_next_node == []


def test_build_summary_always_string():
    builder = HandoffBuilder()
    result = builder.build("agent", {}, {})
    assert isinstance(result.handoff_summary, str)
    result2 = builder.build("agent", 123, {})
    assert isinstance(result2.handoff_summary, str)
