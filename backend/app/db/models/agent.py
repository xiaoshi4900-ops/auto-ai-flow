from __future__ import annotations

from sqlalchemy import String, Integer, Text, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

agent_skill_assoc = Table(
    "agent_skill_assoc",
    Base.metadata,
    Column("agent_id", Integer, ForeignKey("agents.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)

agent_tool_assoc = Table(
    "agent_tool_assoc",
    Base.metadata,
    Column("agent_id", Integer, ForeignKey("agents.id", ondelete="CASCADE"), primary_key=True),
    Column("tool_id", Integer, ForeignKey("tools.id", ondelete="CASCADE"), primary_key=True),
)


class Agent(Base, TimestampMixin):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    role_name: Mapped[str] = mapped_column(String(64), default="assistant")
    system_prompt: Mapped[str | None] = mapped_column(Text)
    background_identity: Mapped[str | None] = mapped_column(Text)
    background_experience: Mapped[str | None] = mapped_column(Text)
    domain_knowledge: Mapped[str | None] = mapped_column(Text)
    responsibility: Mapped[str | None] = mapped_column(Text)
    constraints: Mapped[str | None] = mapped_column(Text)
    model_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    allow_tool_use: Mapped[bool] = mapped_column(Boolean, default=False)
    role_template_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("role_templates.id", ondelete="SET NULL"), nullable=True)
    description: Mapped[str | None] = mapped_column(Text)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    project: Mapped["Project"] = relationship(back_populates="agents")
    skills: Mapped[list["Skill"]] = relationship(secondary=agent_skill_assoc, back_populates="agents")
    tools: Mapped[list["Tool"]] = relationship(secondary=agent_tool_assoc, back_populates="agents")
