from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import String, Integer, Text, Float, ForeignKey, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class WorkflowRun(Base, TimestampMixin):
    __tablename__ = "workflow_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workflow_id: Mapped[int] = mapped_column(Integer, ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(16), default="pending", nullable=False)
    input_payload: Mapped[dict | None] = mapped_column(JSON)
    output_payload: Mapped[dict | None] = mapped_column(JSON)
    error_message: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime | None] = mapped_column()
    finished_at: Mapped[datetime | None] = mapped_column()

    node_runs: Mapped[list["NodeRun"]] = relationship(back_populates="workflow_run", cascade="all, delete-orphan")
    artifacts: Mapped[list["RunArtifact"]] = relationship(back_populates="workflow_run", cascade="all, delete-orphan")


class NodeRun(Base, TimestampMixin):
    __tablename__ = "node_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workflow_run_id: Mapped[int] = mapped_column(Integer, ForeignKey("workflow_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    node_key: Mapped[str] = mapped_column(String(64), nullable=False)
    node_type: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="pending", nullable=False)
    input_data: Mapped[dict | None] = mapped_column(JSON)
    output_data: Mapped[dict | None] = mapped_column(JSON)
    error_message: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime | None] = mapped_column()
    finished_at: Mapped[datetime | None] = mapped_column()
    duration_ms: Mapped[float | None] = mapped_column(Float)

    workflow_run: Mapped["WorkflowRun"] = relationship(back_populates="node_runs")

    __table_args__ = (Index("ix_node_run_workflow_key", "workflow_run_id", "node_key"),)


class RunArtifact(Base, TimestampMixin):
    __tablename__ = "run_artifacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workflow_run_id: Mapped[int] = mapped_column(Integer, ForeignKey("workflow_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    node_key: Mapped[str] = mapped_column(String(64), nullable=False)
    artifact_type: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    content: Mapped[dict | None] = mapped_column(JSON)
    storage_path: Mapped[str | None] = mapped_column(String(512))

    workflow_run: Mapped["WorkflowRun"] = relationship(back_populates="artifacts")
