from app.runtime.condition_evaluator import ConditionEvaluator
from app.schemas.runtime import RuntimeContextSchema


def _make_context(**kwargs):
    defaults = {"input": {}, "shared_state": {}, "node_outputs": {}, "artifacts": {}, "messages": {}, "meta": {}}
    defaults.update(kwargs)
    return RuntimeContextSchema(**defaults)


def test_equals():
    evaluator = ConditionEvaluator()
    ctx = _make_context(input={"score": 80})
    result = evaluator.evaluate({"left_operand": "input.score", "operator": "equals", "right_operand": 80}, ctx)
    assert result is True


def test_not_equals():
    evaluator = ConditionEvaluator()
    ctx = _make_context(input={"score": 80})
    result = evaluator.evaluate({"left_operand": "input.score", "operator": "not_equals", "right_operand": 90}, ctx)
    assert result is True


def test_contains():
    evaluator = ConditionEvaluator()
    ctx = _make_context(input={"text": "hello world"})
    result = evaluator.evaluate({"left_operand": "input.text", "operator": "contains", "right_operand": "world"}, ctx)
    assert result is True


def test_greater_than():
    evaluator = ConditionEvaluator()
    ctx = _make_context(input={"score": 80})
    result = evaluator.evaluate({"left_operand": "input.score", "operator": "greater_than", "right_operand": 60}, ctx)
    assert result is True


def test_less_than():
    evaluator = ConditionEvaluator()
    ctx = _make_context(input={"score": 30})
    result = evaluator.evaluate({"left_operand": "input.score", "operator": "less_than", "right_operand": 60}, ctx)
    assert result is True


def test_exists():
    evaluator = ConditionEvaluator()
    ctx = _make_context(input={"key": "value"})
    result = evaluator.evaluate({"left_operand": "input.key", "operator": "exists", "right_operand": None}, ctx)
    assert result is True


def test_not_exists():
    evaluator = ConditionEvaluator()
    ctx = _make_context(input={})
    result = evaluator.evaluate({"left_operand": "input.missing", "operator": "not_exists", "right_operand": None}, ctx)
    assert result is True


def test_unknown_operator():
    evaluator = ConditionEvaluator()
    ctx = _make_context(input={"x": 1})
    result = evaluator.evaluate({"left_operand": "input.x", "operator": "invalid_op", "right_operand": 1}, ctx)
    assert result is False


def test_resolve_node_outputs():
    evaluator = ConditionEvaluator()
    ctx = _make_context(node_outputs={"agent_1": {"structured_output": {"score": 90}}})
    result = evaluator.evaluate({"left_operand": "node_outputs.agent_1.structured_output.score", "operator": "greater_than", "right_operand": 60}, ctx)
    assert result is True
