from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.repositories.run_repo import RunRepository
from app.db.repositories.workflow_repo import WorkflowRepository
from app.runtime.node_executor_factory import NodeExecutorFactory
from app.runtime.context_manager import ContextManager
from app.schemas.runtime import RuntimeContextSchema
from app.core.constants import NODE_TYPE_START, NODE_TYPE_CONDITION, RUN_STATUS_RUNNING, RUN_STATUS_SUCCESS, RUN_STATUS_FAILED
from app.core.logging import get_logger

logger = get_logger(__name__)


class WorkflowExecutor:
    def __init__(self, db: Session):
        self.db = db
        self.run_repo = RunRepository(db)
        self.workflow_repo = WorkflowRepository(db)
        self.executor_factory = NodeExecutorFactory()
        self.context_manager = ContextManager()

    def execute(self, workflow_run_id: int) -> dict:
        # 1) Load run and mark it running before any node execution.
        run = self.run_repo.get_run_by_id(workflow_run_id)
        if not run:
            logger.error(f"WorkflowRun {workflow_run_id} not found")
            return {"workflow_run_id": workflow_run_id, "status": "failed", "final_output": {}}

        self.run_repo.update_run_status(run, RUN_STATUS_RUNNING)
        run.started_at = datetime.now(timezone.utc)

        workflow = self.workflow_repo.get_by_id(run.workflow_id)
        if not workflow:
            self.run_repo.update_run_status(run, RUN_STATUS_FAILED, error_message="Workflow not found")
            return {"workflow_run_id": workflow_run_id, "status": "failed", "final_output": {}}

        # Runtime context is the only cross-node data carrier in one run.
        context = self.context_manager.init_context(run.input_payload or {})

        nodes = {n.node_key: n for n in workflow.nodes}
        edges = workflow.edges

        adjacency = {}
        for edge in edges:
            adjacency.setdefault(edge.source_node_key, []).append(edge)

        start_node = next((n for n in workflow.nodes if n.node_type == NODE_TYPE_START), None)
        if not start_node:
            self.run_repo.update_run_status(run, RUN_STATUS_FAILED, error_message="No start node found")
            return {"workflow_run_id": workflow_run_id, "status": "failed", "final_output": {}}

        current_key = start_node.node_key
        visited = set()

        # Main execution loop:
        # - follows directed edges node by node
        # - stops on end-of-graph or cycle detection
        while current_key and current_key not in visited:
            visited.add(current_key)
            node = nodes.get(current_key)
            if not node:
                logger.error(f"Node {current_key} not found in workflow")
                break

            node_run = self.run_repo.create_node_run(
                workflow_run_id=run.id,
                node_key=node.node_key,
                node_type=node.node_type,
                input_data=context.node_outputs if context.node_outputs else context.input,
            )

            try:
                executor = self.executor_factory.get_executor(node.node_type)
                result = executor.execute(run, node, context)
                # Merge current node output back into shared runtime context.
                context = self.context_manager.merge_node_result(context, node.node_key, result)

                self.run_repo.update_node_run(
                    node_run,
                    status=result.status,
                    output_data=result.output.model_dump() if result.output else None,
                    finished_at=datetime.now(timezone.utc),
                    duration_ms=(datetime.now(timezone.utc) - node_run.started_at).total_seconds() * 1000 if node_run.started_at else 0,
                )

                if result.status == "failed":
                    self.run_repo.update_run_status(run, RUN_STATUS_FAILED, error_message=result.error_message)
                    return {"workflow_run_id": workflow_run_id, "status": "failed", "final_output": {}}

                # Condition nodes can explicitly route to a branch target;
                # all other nodes follow the first outgoing edge.
                if node.node_type == NODE_TYPE_CONDITION and result.next_node_key:
                    current_key = result.next_node_key
                else:
                    next_edges = adjacency.get(current_key, [])
                    if next_edges:
                        current_key = next_edges[0].target_node_key
                    else:
                        current_key = None

            except Exception as e:
                logger.exception(f"Error executing node {current_key}")
                self.run_repo.update_node_run(node_run, status="failed", error_message=str(e), finished_at=datetime.now(timezone.utc))
                self.run_repo.update_run_status(run, RUN_STATUS_FAILED, error_message=str(e))
                return {"workflow_run_id": workflow_run_id, "status": "failed", "final_output": {}}

        final_output = context.node_outputs
        self.run_repo.update_run_status(run, RUN_STATUS_SUCCESS, output_payload=final_output)
        run.finished_at = datetime.now(timezone.utc)
        self.db.commit()

        return {"workflow_run_id": workflow_run_id, "status": "success", "final_output": final_output}
