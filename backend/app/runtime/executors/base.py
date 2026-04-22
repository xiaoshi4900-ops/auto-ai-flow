from typing import Protocol

from app.schemas.runtime import RuntimeContextSchema, NodeExecutionResultSchema
from app.db.models.run import WorkflowRun
from app.db.models.workflow import WorkflowNode


class BaseNodeExecutor(Protocol):
    def execute(self, workflow_run: WorkflowRun, workflow_node: WorkflowNode, runtime_context: RuntimeContextSchema) -> NodeExecutionResultSchema: ...
