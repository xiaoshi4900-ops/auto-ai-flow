from sqlalchemy.orm import Session

from app.db.repositories.workflow_repo import WorkflowRepository
from app.db.repositories.project_repo import ProjectRepository
from app.schemas.workflow import WorkflowCreateRequest, WorkflowUpdateRequest, WorkflowResponse, WorkflowListResponse, WorkflowNodeSchema, WorkflowEdgeSchema
from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException
from app.core.constants import VALID_NODE_TYPES


class WorkflowService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = WorkflowRepository(db)
        self.project_repo = ProjectRepository(db)

    def _check_project_owner(self, project_id: int, user_id: int):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise NotFoundException("Project")
        if project.owner_id != user_id:
            raise ForbiddenException("Not project owner")

    def _validate_workflow(self, nodes: list[WorkflowNodeSchema], edges: list[WorkflowEdgeSchema]):
        for node in nodes:
            if node.node_type not in VALID_NODE_TYPES:
                raise BadRequestException(f"Invalid node_type: {node.node_type}")
        start_nodes = [n for n in nodes if n.node_type == "start"]
        if len(start_nodes) != 1:
            raise BadRequestException("Workflow must contain exactly one start node")
        node_keys = {n.node_key for n in nodes}
        seen_edges = set()
        for edge in edges:
            if edge.source_node_key not in node_keys or edge.target_node_key not in node_keys:
                raise BadRequestException(f"Edge references non-existent node: {edge.source_node_key} -> {edge.target_node_key}")
            if edge.source_node_key == edge.target_node_key:
                raise BadRequestException(f"Self loop is not allowed: {edge.source_node_key}")
            edge_key = (edge.source_node_key, edge.target_node_key)
            if edge_key in seen_edges:
                raise BadRequestException(f"Duplicate edge is not allowed: {edge.source_node_key} -> {edge.target_node_key}")
            seen_edges.add(edge_key)

    def create(self, req: WorkflowCreateRequest, user_id: int) -> WorkflowResponse:
        self._check_project_owner(req.project_id, user_id)
        self._validate_workflow(req.nodes, req.edges)
        nodes_data = [n.model_dump() for n in req.nodes]
        edges_data = [e.model_dump() for e in req.edges]
        workflow = self.repo.create(project_id=req.project_id, name=req.name, description=req.description, nodes=nodes_data, edges=edges_data)
        return self._to_response(workflow)

    def get(self, workflow_id: int, user_id: int) -> WorkflowResponse:
        workflow = self.repo.get_by_id(workflow_id)
        if not workflow:
            raise NotFoundException("Workflow")
        self._check_project_owner(workflow.project_id, user_id)
        return self._to_response(workflow)

    def list_by_project(self, project_id: int, user_id: int, page: int = 1, page_size: int = 20) -> WorkflowListResponse:
        self._check_project_owner(project_id, user_id)
        items, total = self.repo.list_by_project(project_id, page, page_size)
        return WorkflowListResponse(total=total, items=[self._to_response(w) for w in items])

    def update(self, workflow_id: int, req: WorkflowUpdateRequest, user_id: int) -> WorkflowResponse:
        workflow = self.repo.get_by_id(workflow_id)
        if not workflow:
            raise NotFoundException("Workflow")
        self._check_project_owner(workflow.project_id, user_id)
        update_data = req.model_dump(exclude_unset=True)
        next_nodes = req.nodes if req.nodes is not None else [
            WorkflowNodeSchema(
                node_key=n.node_key,
                node_type=n.node_type,
                label=n.label,
                config=n.config or {},
                position_x=n.position_x,
                position_y=n.position_y,
            )
            for n in workflow.nodes
        ]
        next_edges = req.edges if req.edges is not None else [
            WorkflowEdgeSchema(
                source_node_key=e.source_node_key,
                target_node_key=e.target_node_key,
                condition=e.condition,
                label=e.label,
            )
            for e in workflow.edges
        ]
        if req.nodes is not None or req.edges is not None:
            self._validate_workflow(next_nodes, next_edges)
        if req.nodes is not None:
            update_data["nodes"] = [n.model_dump() for n in req.nodes]
        if req.edges is not None:
            update_data["edges"] = [e.model_dump() for e in req.edges]
        updated = self.repo.update(workflow, **update_data)
        return self._to_response(updated)

    def delete(self, workflow_id: int, user_id: int) -> None:
        workflow = self.repo.get_by_id(workflow_id)
        if not workflow:
            raise NotFoundException("Workflow")
        self._check_project_owner(workflow.project_id, user_id)
        self.repo.soft_delete(workflow)

    def _to_response(self, workflow) -> WorkflowResponse:
        nodes = [WorkflowNodeSchema(
            node_key=n.node_key,
            node_type=n.node_type,
            label=n.label,
            config=n.config or {},
            position_x=n.position_x,
            position_y=n.position_y,
        ) for n in workflow.nodes] if workflow.nodes else []
        edges = [WorkflowEdgeSchema(
            source_node_key=e.source_node_key,
            target_node_key=e.target_node_key,
            condition=e.condition,
            label=e.label,
        ) for e in workflow.edges] if workflow.edges else []
        return WorkflowResponse(
            id=workflow.id,
            project_id=workflow.project_id,
            name=workflow.name,
            description=workflow.description,
            nodes=nodes,
            edges=edges,
            canvas_data=workflow.canvas_data,
            created_at=workflow.created_at,
            updated_at=workflow.updated_at,
        )
