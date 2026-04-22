from __future__ import annotations

from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class CodeIteration(Base, TimestampMixin):
    __tablename__ = "code_iterations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code_task_id: Mapped[int] = mapped_column(Integer, ForeignKey("code_tasks.id", ondelete="CASCADE"), nullable=False)
    iteration_no: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="running")
    plan_summary: Mapped[str | None] = mapped_column(Text)
    changed_files: Mapped[str | None] = mapped_column(Text)
    artifact_refs: Mapped[str | None] = mapped_column(Text)
    validation_lint: Mapped[str | None] = mapped_column(String(16))
    validation_build: Mapped[str | None] = mapped_column(String(16))
    validation_unit_tests: Mapped[str | None] = mapped_column(String(16))
    open_issues: Mapped[str | None] = mapped_column(Text)
    next_actions: Mapped[str | None] = mapped_column(Text)

    code_task: Mapped["CodeTask"] = relationship(back_populates="iterations")
