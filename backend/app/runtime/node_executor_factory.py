from app.runtime.executors.base import BaseNodeExecutor
from app.runtime.executors.start_node import StartNodeExecutor
from app.runtime.executors.input_node import InputNodeExecutor
from app.runtime.executors.agent_node import AgentNodeExecutor
from app.runtime.executors.condition_node import ConditionNodeExecutor
from app.runtime.executors.output_node import OutputNodeExecutor
from app.runtime.executors.tool_node import ToolNodeExecutor
from app.core.constants import NODE_TYPE_START, NODE_TYPE_INPUT, NODE_TYPE_AGENT, NODE_TYPE_CONDITION, NODE_TYPE_OUTPUT, NODE_TYPE_TOOL
from app.core.exceptions import BadRequestException


class NodeExecutorFactory:
    _executors: dict[str, BaseNodeExecutor] = {}

    def __init__(self):
        self._executors = {
            NODE_TYPE_START: StartNodeExecutor(),
            NODE_TYPE_INPUT: InputNodeExecutor(),
            NODE_TYPE_AGENT: AgentNodeExecutor(),
            NODE_TYPE_CONDITION: ConditionNodeExecutor(),
            NODE_TYPE_OUTPUT: OutputNodeExecutor(),
            NODE_TYPE_TOOL: ToolNodeExecutor(),
        }

    def get_executor(self, node_type: str) -> BaseNodeExecutor:
        executor = self._executors.get(node_type)
        if not executor:
            raise BadRequestException(f"Unsupported node_type: {node_type}")
        return executor
