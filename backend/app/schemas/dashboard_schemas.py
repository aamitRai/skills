"""
Dashboard API schemas.

Pydantic models for dashboard summary response and activity feed.
"""

from datetime import datetime

from pydantic import BaseModel


class RecentlyUpdatedSkill(BaseModel):
    """Summary of a recently updated skill."""

    skill_id: str
    skill_name: str
    category_name: str
    progress: int
    last_updated: datetime


class ActivityItem(BaseModel):
    """Single activity log entry."""

    id: str
    type: str  # 'progress-update', 'skill-created', 'skill-completed', 'comment-added'
    skill_id: str
    skill_name: str
    category_name: str
    description: str
    timestamp: datetime


class DashboardSummaryResponse(BaseModel):
    """Dashboard summary payload."""

    total_categories: int
    total_skills: int
    completed_skills: int
    in_progress_skills: int
    overall_progress: float
    recently_updated: list[RecentlyUpdatedSkill] = []
