from __future__ import annotations

from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.agent import agent_skill_assoc


class Skill(Base, TimestampMixin):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    skill_key: Mapped[str | None] = mapped_column(String(128))
    description: Mapped[str | None] = mapped_column(Text)
    prompt_template: Mapped[str | None] = mapped_column(Text)
    execution_mode: Mapped[str | None] = mapped_column(String(32))
    is_builtin: Mapped[bool] = mapped_column(default=False)

    agents: Mapped[list["Agent"]] = relationship(secondary=agent_skill_assoc, back_populates="skills")
