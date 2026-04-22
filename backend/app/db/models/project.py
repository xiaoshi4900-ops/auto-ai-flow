from __future__ import annotations

from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    default_model_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    agents: Mapped[list["Agent"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    workflows: Mapped[list["Workflow"]] = relationship(back_populates="project", cascade="all, delete-orphan")
