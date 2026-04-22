from __future__ import annotations

from sqlalchemy import String, Integer, Text, Boolean, ForeignKey, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Workflow(Base, TimestampMixin):
    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    canvas_data: Mapped[dict | None] = mapped_column(JSON)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    project: Mapped["Project"] = relationship(back_populates="workflows")
    nodes: Mapped[list["WorkflowNode"]] = relationship(back_populates="workflow", cascade="all, delete-orphan")
    edges: Mapped[list["WorkflowEdge"]] = relationship(back_populates="workflow", cascade="all, delete-orphan")


class WorkflowNode(Base, TimestampMixin):
    __tablename__ = "workflow_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workflow_id: Mapped[int] = mapped_column(Integer, ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    node_key: Mapped[str] = mapped_column(String(64), nullable=False)
    node_type: Mapped[str] = mapped_column(String(32), nullable=False)
    label: Mapped[str | None] = mapped_column(String(128))
    config: Mapped[dict | None] = mapped_column(JSON)
    position_x: Mapped[float | None] = mapped_column()
    position_y: Mapped[float | None] = mapped_column()

    workflow: Mapped["Workflow"] = relationship(back_populates="nodes")

    __table_args__ = (Index("ix_workflow_node_key", "workflow_id", "node_key", unique=True),)


class WorkflowEdge(Base, TimestampMixin):
    __tablename__ = "workflow_edges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workflow_id: Mapped[int] = mapped_column(Integer, ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    source_node_key: Mapped[str] = mapped_column(String(64), nullable=False)
    target_node_key: Mapped[str] = mapped_column(String(64), nullable=False)
    condition: Mapped[dict | None] = mapped_column(JSON)
    label: Mapped[str | None] = mapped_column(String(128))

    workflow: Mapped["Workflow"] = relationship(back_populates="edges")
