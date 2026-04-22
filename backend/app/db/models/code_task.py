from __future__ import annotations

from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class CodeTask(Base, TimestampMixin):
    __tablename__ = "code_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workflow_run_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("workflow_runs.id", ondelete="SET NULL"), nullable=True)
    node_run_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("node_runs.id", ondelete="SET NULL"), nullable=True)
    agent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("agents.id", ondelete="SET NULL"), nullable=True)
    task_goal: Mapped[str | None] = mapped_column(Text)
    scope: Mapped[str | None] = mapped_column(Text)
    acceptance_criteria: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="running")

    iterations: Mapped[list["CodeIteration"]] = relationship(back_populates="code_task", order_by="CodeIteration.iteration_no")
