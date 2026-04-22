from __future__ import annotations

from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.agent import agent_tool_assoc


class Tool(Base, TimestampMixin):
    __tablename__ = "tools"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    tool_type: Mapped[str] = mapped_column(String(32), default="function")
    config: Mapped[str | None] = mapped_column(Text)
    is_builtin: Mapped[bool] = mapped_column(default=False)

    agents: Mapped[list["Agent"]] = relationship(secondary=agent_tool_assoc, back_populates="tools")
