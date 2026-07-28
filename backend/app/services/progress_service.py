"""Progress service."""

import logging
from datetime import datetime, timezone

from app.constants import log_messages as log
from app.models.progress import SkillProgressInDB
from app.repositories.progress_repository import ProgressRepository
from app.schemas.progress_schemas import ProgressResponse, ProgressUpdateRequest

logger = logging.getLogger(__name__)


def compute_status(progress: int) -> str:
    """Compute progress status from a percentage value."""
    if progress == 0:
        return "not-started"
    if progress >= 100:
        return "completed"
    return "in-progress"


class ProgressService:
    """Business logic for skill progress management."""

    def __init__(self, progress_repo: ProgressRepository) -> None:
        self._progress_repo = progress_repo

    async def get_by_skill_id(self, skill_id: str) -> ProgressResponse:
        """Get progress for a specific skill.

        Args:
            skill_id: The skill's ID.

        Returns:
            ProgressResponse (returns zero progress if no record exists).
        """
        record = await self._progress_repo.find_by_skill_id(skill_id)
        if record is None:
            return ProgressResponse(
                skill_id=skill_id,
                progress=0,
                status="not-started",
                last_updated=datetime.now(timezone.utc),
            )
        return ProgressResponse(
            skill_id=record.skill_id,
            progress=record.progress,
            status=record.status,
            last_updated=record.last_updated,
        )

    async def get_all(self) -> list[ProgressResponse]:
        """Get all progress records.

        Returns:
            List of ProgressResponse.
        """
        records = await self._progress_repo.find_all()
        return [
            ProgressResponse(
                skill_id=r.skill_id,
                progress=r.progress,
                status=r.status,
                last_updated=r.last_updated,
            )
            for r in records
        ]

    async def update(
        self, skill_id: str, payload: ProgressUpdateRequest
    ) -> ProgressResponse:
        """Update progress for a skill, computing status automatically.

        Args:
            skill_id: The skill's ID.
            payload: Progress percentage to set.

        Returns:
            Updated ProgressResponse.
        """
        status = compute_status(payload.progress)
        record = await self._progress_repo.upsert(
            skill_id, payload.progress, status
        )
        logger.info(log.LOG_PROGRESS_UPDATED, skill_id)
        return ProgressResponse(
            skill_id=record.skill_id,
            progress=record.progress,
            status=record.status,
            last_updated=record.last_updated,
        )
