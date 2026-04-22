from __future__ import annotations

from sqlalchemy import String, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class CodeExecutionPolicy(Base, TimestampMixin):
    __tablename__ = "code_execution_policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_template_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("role_templates.id", ondelete="SET NULL"), nullable=True)
    project_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    max_iterations: Mapped[int] = mapped_column(Integer, default=3)
    allow_file_write: Mapped[bool] = mapped_column(Boolean, default=False)
    run_lint: Mapped[bool] = mapped_column(Boolean, default=True)
    run_build: Mapped[bool] = mapped_column(Boolean, default=False)
    run_unit_tests: Mapped[bool] = mapped_column(Boolean, default=True)
    require_plan_first: Mapped[bool] = mapped_column(Boolean, default=True)
    require_integration_tests: Mapped[bool] = mapped_column(Boolean, default=False)
    allow_repo_read: Mapped[bool] = mapped_column(Boolean, default=True)
    allow_repo_write: Mapped[bool] = mapped_column(Boolean, default=False)
    allow_auto_commit: Mapped[bool] = mapped_column(Boolean, default=False)
    allow_auto_pr: Mapped[bool] = mapped_column(Boolean, default=False)
    stop_on_critical_error: Mapped[bool] = mapped_column(Boolean, default=True)
    fallback_to_human: Mapped[bool] = mapped_column(Boolean, default=True)
