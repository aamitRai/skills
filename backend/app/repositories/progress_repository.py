"""Progress repository — Beanie async data access."""

import logging
from datetime import datetime, timezone

from app.models.progress import SkillProgress

logger = logging.getLogger(__name__)


class ProgressRepository:
    """Data access layer for progress documents."""

    async def find_by_skill_id(self, skill_id: str) -> SkillProgress | None:
        """Find progress record for a specific skill."""
        return await SkillProgress.find_one(SkillProgress.skill_id == skill_id)

    async def find_all(self) -> list[SkillProgress]:
        """Find all progress records."""
        return await SkillProgress.find_all().to_list()

    async def upsert(
        self, skill_id: str, progress: float, status: str
    ) -> SkillProgress:
        """Insert or update a progress record for a skill."""
        record = await self.find_by_skill_id(skill_id)
        if record is not None:
            record.progress = progress
            record.status = status
            record.last_updated = datetime.now(timezone.utc)
            await record.save()
        else:
            record = SkillProgress(
                skill_id=skill_id,
                progress=progress,
                status=status,
                last_updated=datetime.now(timezone.utc),
            )
            await record.create()
        logger.info("Progress upserted", extra={"skill_id": skill_id})
        return record

    async def delete_by_skill_id(self, skill_id: str) -> bool:
        """Delete progress record for a skill."""
        record = await self.find_by_skill_id(skill_id)
        if record is None:
            return False
        await record.delete()
        return True

    async def delete_many(self, skill_ids: list[str]) -> int:
        """Delete progress records for multiple skills."""
        deleted = 0
        for sid in skill_ids:
            record = await self.find_by_skill_id(sid)
            if record is not None:
                await record.delete()
                deleted += 1
        return deleted
