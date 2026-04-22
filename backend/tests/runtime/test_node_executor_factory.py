import pytest
from app.runtime.node_executor_factory import NodeExecutorFactory
from app.runtime.executors.start_node import StartNodeExecutor
from app.runtime.executors.input_node import InputNodeExecutor
from app.runtime.executors.agent_node import AgentNodeExecutor
from app.runtime.executors.condition_node import ConditionNodeExecutor
from app.runtime.executors.output_node import OutputNodeExecutor
from app.core.exceptions import BadRequestException


def test_factory_returns_start():
    factory = NodeExecutorFactory()
    executor = factory.get_executor("start")
    assert isinstance(executor, StartNodeExecutor)


def test_factory_returns_input():
    factory = NodeExecutorFactory()
    executor = factory.get_executor("input")
    assert isinstance(executor, InputNodeExecutor)


def test_factory_returns_agent():
    factory = NodeExecutorFactory()
    executor = factory.get_executor("agent")
    assert isinstance(executor, AgentNodeExecutor)


def test_factory_returns_condition():
    factory = NodeExecutorFactory()
    executor = factory.get_executor("condition")
    assert isinstance(executor, ConditionNodeExecutor)


def test_factory_returns_output():
    factory = NodeExecutorFactory()
    executor = factory.get_executor("output")
    assert isinstance(executor, OutputNodeExecutor)


def test_factory_unknown_type_raises():
    factory = NodeExecutorFactory()
    with pytest.raises(BadRequestException):
        factory.get_executor("unknown_type")
