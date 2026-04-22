from __future__ import annotations

from sqlalchemy import String, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class RoleTemplate(Base, TimestampMixin):
    __tablename__ = "role_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str | None] = mapped_column(String(64))
    description: Mapped[str | None] = mapped_column(Text)
    execution_mode: Mapped[str] = mapped_column(String(32), default="normal_llm")
    default_role_name: Mapped[str | None] = mapped_column(String(128))
    default_model_id: Mapped[int | None] = mapped_column(Integer)
    default_skill_ids: Mapped[str | None] = mapped_column(Text)
    default_tool_ids: Mapped[str | None] = mapped_column(Text)
    policy_config: Mapped[str | None] = mapped_column(Text)
    is_builtin: Mapped[bool] = mapped_column(Boolean, default=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
