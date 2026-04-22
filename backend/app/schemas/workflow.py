from datetime import datetime

from pydantic import BaseModel, Field


class AgentNodeConfigSchema(BaseModel):
    agent_id: int
    task_instruction: str = ""
    input_mapping: dict = Field(default_factory=dict)
    allowed_skill_ids: list[int] = Field(default_factory=list)
    allow_tool_use: bool = False
    model_override_id: int | None = None
    retry_limit: int = 0
    force_execution_mode: str | None = None
    code_policy_override: dict | None = None
    workspace_binding: dict | None = None


class ConditionBranchSchema(BaseModel):
    expression_type: str = "simple"
    left_operand: str = ""
    operator: str = "equals"
    right_operand: str | int | float | bool | None = None
    target_node_key: str = ""


class ConditionNodeConfigSchema(BaseModel):
    branches: list[ConditionBranchSchema] = Field(default_factory=list)
    default_target_key: str = ""


class OutputNodeConfigSchema(BaseModel):
    source_keys: list[str] = Field(default_factory=list)
    output_format: str = "raw"


class ToolNodeConfigSchema(BaseModel):
    tool_id: int
    input_mapping: dict = Field(default_factory=dict)
    retry_limit: int = 0


class WorkflowNodeSchema(BaseModel):
    node_key: str
    node_type: str
    label: str | None = None
    config: dict = Field(default_factory=dict)
    position_x: float | None = None
    position_y: float | None = None


class WorkflowEdgeSchema(BaseModel):
    source_node_key: str
    target_node_key: str
    condition: dict | None = None
    label: str | None = None


class WorkflowCreateRequest(BaseModel):
    project_id: int
    name: str
    description: str | None = None
    nodes: list[WorkflowNodeSchema] = Field(default_factory=list)
    edges: list[WorkflowEdgeSchema] = Field(default_factory=list)


class WorkflowUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    nodes: list[WorkflowNodeSchema] | None = None
    edges: list[WorkflowEdgeSchema] | None = None
    canvas_data: dict | None = None


class WorkflowResponse(BaseModel):
    id: int
    project_id: int
    name: str
    description: str | None = None
    nodes: list[WorkflowNodeSchema] = Field(default_factory=list)
    edges: list[WorkflowEdgeSchema] = Field(default_factory=list)
    canvas_data: dict | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class WorkflowListResponse(BaseModel):
    total: int
    items: list[WorkflowResponse]
