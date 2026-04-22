from __future__ import annotations

from sqlalchemy import String, Integer, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class ModelProvider(Base, TimestampMixin):
    __tablename__ = "model_providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    provider_type: Mapped[str] = mapped_column(String(32), nullable=False)
    api_base: Mapped[str | None] = mapped_column(String(512))
    is_builtin: Mapped[bool] = mapped_column(default=False)

    models: Mapped[list["ModelDefinition"]] = relationship(back_populates="provider", cascade="all, delete-orphan")


class ModelDefinition(Base, TimestampMixin):
    __tablename__ = "model_definitions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider_id: Mapped[int] = mapped_column(Integer, ForeignKey("model_providers.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    model_id: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    capabilities: Mapped[dict | None] = mapped_column(JSON)
    is_builtin: Mapped[bool] = mapped_column(default=False)

    provider: Mapped["ModelProvider"] = relationship(back_populates="models")


class ProjectModelConfig(Base, TimestampMixin):
    __tablename__ = "project_model_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    model_definition_id: Mapped[int] = mapped_column(Integer, ForeignKey("model_definitions.id", ondelete="CASCADE"), nullable=False)
    api_key_encrypted: Mapped[str | None] = mapped_column(Text)
    custom_config: Mapped[dict | None] = mapped_column(JSON)
    is_default: Mapped[bool] = mapped_column(default=False)
