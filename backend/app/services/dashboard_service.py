"""Dashboard service."""

import logging
from datetime import datetime

from app.constants import log_messages as log
from app.repositories.category_repository import CategoryRepository
from app.repositories.comment_repository import CommentRepository
from app.repositories.progress_repository import ProgressRepository
from app.schemas.dashboard_schemas import (
    ActivityItem,
    DashboardSummaryResponse,
    RecentlyUpdatedSkill,
)

logger = logging.getLogger(__name__)


class DashboardService:
    """Business logic for dashboard summary data and activity feed."""

    def __init__(
        self,
        category_repo: CategoryRepository,
        progress_repo: ProgressRepository,
        comment_repo: CommentRepository | None = None,
    ) -> None:
        self._category_repo = category_repo
        self._progress_repo = progress_repo
        self._comment_repo = comment_repo

    async def get_summary(self, user_id: str) -> DashboardSummaryResponse:
        """Compute and return the dashboard summary for a user.

        Args:
            user_id: The authenticated user's ID.

        Returns:
            DashboardSummaryResponse with aggregated statistics.
        """
        categories = await self._category_repo.find_all_by_user(user_id)
        all_progress = await self._progress_repo.find_all()

        progress_map: dict[str, int] = {p.skill_id: p.progress for p in all_progress}
        status_map: dict[str, str] = {p.skill_id: p.status for p in all_progress}
        last_updated_map: dict[str, datetime] = {
            p.skill_id: p.last_updated for p in all_progress
        }

        total_skills = 0
        completed_skills = 0
        in_progress_skills = 0
        total_progress = 0
        recently_updated: list[RecentlyUpdatedSkill] = []

        for category in categories:
            skills = await self._category_repo.find_skills_by_category(str(category.id))
            for skill in skills:
                total_skills += 1
                progress = progress_map.get(str(skill.id), 0)
                total_progress += progress

                status = status_map.get(str(skill.id), "not-started")
                if status == "completed":
                    completed_skills += 1
                elif status == "in-progress":
                    in_progress_skills += 1

                last_updated = last_updated_map.get(str(skill.id))
                if last_updated is not None:
                    recently_updated.append(
                        RecentlyUpdatedSkill(
                            skill_id=str(skill.id),
                            skill_name=skill.name,
                            category_name=category.name,
                            progress=progress,
                            last_updated=last_updated,
                        )
                    )

        recently_updated.sort(key=lambda x: x.last_updated, reverse=True)
        recently_updated = recently_updated[:10]

        overall_progress = (total_progress / total_skills) if total_skills > 0 else 0.0

        logger.info(log.LOG_DASHBOARD_SUMMARY_COMPUTED, user_id)
        return DashboardSummaryResponse(
            total_categories=len(categories),
            total_skills=total_skills,
            completed_skills=completed_skills,
            in_progress_skills=in_progress_skills,
            overall_progress=round(overall_progress, 2),
            recently_updated=recently_updated,
        )

    async def get_activity(self, user_id: str) -> list[ActivityItem]:
        """Build a recent activity feed for a user.

        Aggregates progress updates, skill creation, and comment activity
        sorted by most recent first.

        Args:
            user_id: The authenticated user's ID.

        Returns:
            List of ActivityItem sorted by timestamp descending.
        """
        categories = await self._category_repo.find_all_by_user(user_id)
        all_progress = await self._progress_repo.find_all()

        activity: list[ActivityItem] = []

        skill_map: dict[str, tuple[str, str]] = {}
        for category in categories:
            skills = await self._category_repo.find_skills_by_category(str(category.id))
            for skill in skills:
                skill_map[str(skill.id)] = (skill.name, category.name)

        for progress in all_progress:
            if progress.skill_id not in skill_map:
                continue
            skill_name, category_name = skill_map[progress.skill_id]

            activity.append(
                ActivityItem(
                    id=f"progress-{progress.skill_id}",
                    type="progress-update",
                    skill_id=str(progress.skill_id),
                    skill_name=skill_name,
                    category_name=category_name,
                    description=f"Progress updated to {int(progress.progress)}%",
                    timestamp=progress.last_updated,
                )
            )

            if progress.status == "completed":
                activity.append(
                    ActivityItem(
                        id=f"completed-{progress.skill_id}",
                        type="skill-completed",
                        skill_id=str(progress.skill_id),
                        skill_name=skill_name,
                        category_name=category_name,
                        description=f"Completed {skill_name}",
                        timestamp=progress.last_updated,
                    )
                )

        for category in categories:
            skills = await self._category_repo.find_skills_by_category(str(category.id))
            for skill in skills:
                activity.append(
                    ActivityItem(
                        id=f"created-{skill.id}",
                        type="skill-created",
                        skill_id=str(skill.id),
                        skill_name=skill.name,
                        category_name=category.name,
                        description=f"Created {skill.name} in {category.name}",
                        timestamp=skill.created_at,
                    )
                )

        if self._comment_repo:
            for category in categories:
                skills = await self._category_repo.find_skills_by_category(str(category.id))
                for skill in skills:
                    comments = await self._comment_repo.find_by_skill_id(str(skill.id))
                    for comment in comments:
                        activity.append(
                            ActivityItem(
                                id=f"comment-{comment.id}",
                                type="comment-added",
                                skill_id=str(skill.id),
                                skill_name=skill.name,
                                category_name=category.name,
                                description=f"Added comment to {skill.name}",
                                timestamp=comment.created_at,
                            )
                        )

        activity.sort(key=lambda x: x.timestamp, reverse=True)
        logger.info(log.LOG_ACTIVITY_FEED_COMPUTED, user_id)
        return activity[:50]
