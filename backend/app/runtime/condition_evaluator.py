from app.schemas.runtime import RuntimeContextSchema


class ConditionEvaluator:
    OPERATORS = {
        "equals": lambda a, b: a == b,
        "not_equals": lambda a, b: a != b,
        "contains": lambda a, b: b in a if a else False,
        "greater_than": lambda a, b: a > b,
        "less_than": lambda a, b: a < b,
        "exists": lambda a, b: a is not None,
        "not_exists": lambda a, b: a is None,
    }

    def evaluate(self, branch: dict, context: RuntimeContextSchema) -> bool:
        left_operand = branch.get("left_operand", "")
        operator = branch.get("operator", "equals")
        right_operand = branch.get("right_operand")

        left_value = self._resolve_path(left_operand, context)
        op_func = self.OPERATORS.get(operator)
        if not op_func:
            return False
        try:
            return op_func(left_value, right_operand)
        except (TypeError, ValueError):
            return False

    def _resolve_path(self, path: str, context: RuntimeContextSchema):
        parts = path.split(".")
        if not parts:
            return None
        root = parts[0]
        data_map = {
            "input": context.input,
            "shared_state": context.shared_state,
            "node_outputs": context.node_outputs,
            "artifacts": context.artifacts,
            "messages": context.messages,
            "meta": context.meta,
        }
        value = data_map.get(root)
        for part in parts[1:]:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None
        return value
