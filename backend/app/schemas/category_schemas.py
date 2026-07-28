"""
Category and skill API schemas.

Pydantic models for CRUD request validation and response serialization.
"""

from datetime import datetime

from pydantic import BaseModel, Field


# --- Skill ---

class SkillCreateRequest(BaseModel):
    """Incoming payload to create a skill within a category."""

    name: str = Field(..., min_length=1, max_length=200)
    index: int = Field(default=0, ge=0)
    priority: str = Field(default="medium")
    difficulty: str = Field(default="medium")
    estimated_hours: int | None = Field(default=None, ge=0)


class SkillUpdateRequest(BaseModel):
    """Incoming payload for partial skill update."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    index: int | None = Field(default=None, ge=0)
    priority: str | None = None
    difficulty: str | None = None
    estimated_hours: int | None = Field(default=None, ge=0)


class SkillMoveRequest(BaseModel):
    """Incoming payload to move a skill up or down in display order."""

    direction: str = Field(..., pattern="^(up|down)$")


class SkillResponse(BaseModel):
    """Outgoing skill payload."""

    id: str
    category_id: str
    name: str
    index: int
    priority: str
    difficulty: str
    estimated_hours: int | None = None
    created_at: datetime
    updated_at: datetime


# --- Category ---

class CategoryCreateRequest(BaseModel):
    """Incoming payload to create a category."""

    name: str = Field(..., min_length=1, max_length=200)
    icon: str = Field(default="📁", max_length=10)


class CategoryUpdateRequest(BaseModel):
    """Incoming payload for partial category update."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    icon: str | None = Field(default=None, max_length=10)


class CategoryResponse(BaseModel):
    """Outgoing category payload with nested skills."""

    id: str
    name: str
    icon: str
    skills: list[SkillResponse] = []
    created_at: datetime
    updated_at: datetime
