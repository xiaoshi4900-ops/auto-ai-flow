from datetime import datetime

from pydantic import BaseModel


class ExecutionTriggerRequest(BaseModel):
    workflow_id: int
    input_payload: dict | None = None


class ExecutionTriggerResponse(BaseModel):
    run_id: int
    status: str
    message: str = "Workflow execution triggered"


class RunResponse(BaseModel):
    id: int
    workflow_id: int
    status: str
    input_payload: dict | None = None
    output_payload: dict | None = None
    error_message: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class NodeRunResponse(BaseModel):
    id: int
    workflow_run_id: int
    node_key: str
    node_type: str
    status: str
    input_data: dict | None = None
    output_data: dict | None = None
    error_message: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    duration_ms: float | None = None

    model_config = {"from_attributes": True}


class RunDetailResponse(BaseModel):
    run: RunResponse
    node_runs: list[NodeRunResponse] = []


class RunListResponse(BaseModel):
    total: int
    items: list[RunResponse]
