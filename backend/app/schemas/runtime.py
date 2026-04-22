from typing import Literal

from pydantic import BaseModel, Field


class StructuredOutputSchema(BaseModel):
    status: Literal["success", "failed"] = "success"
    structured_output: dict = Field(default_factory=dict)
    artifact_refs: list[dict] = Field(default_factory=list)
    next_suggestion: dict = Field(default_factory=dict)


class HandoffPayloadSchema(BaseModel):
    handoff_summary: str = ""
    assumptions: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    questions_for_next_node: list[str] = Field(default_factory=list)


class RuntimeContextSchema(BaseModel):
    input: dict = Field(default_factory=dict)
    shared_state: dict = Field(default_factory=dict)
    node_outputs: dict = Field(default_factory=dict)
    artifacts: dict = Field(default_factory=dict)
    messages: dict = Field(default_factory=dict)
    meta: dict = Field(default_factory=dict)


class NodeExecutionResultSchema(BaseModel):
    node_key: str
    node_type: str
    status: Literal["success", "failed"] = "success"
    output: StructuredOutputSchema = Field(default_factory=StructuredOutputSchema)
    handoff: HandoffPayloadSchema = Field(default_factory=HandoffPayloadSchema)
    next_node_key: str | None = None
    error_message: str | None = None
