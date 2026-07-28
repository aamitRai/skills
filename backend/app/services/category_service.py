"""Category service."""

import logging

from app.constants import log_messages as log
from app.constants import error_messages as err
from app.exceptions.app_exceptions import (
    CategoryNotFoundError,
    DuplicateError,
    SkillNotFoundError,
)
from app.models.category import CategoryInDB, SkillInDB
from app.repositories.category_repository import CategoryRepository
from app.repositories.comment_repository import CommentRepository
from app.repositories.progress_repository import ProgressRepository
from app.schemas.category_schemas import (
    CategoryCreateRequest,
    CategoryResponse,
    CategoryUpdateRequest,
    SkillCreateRequest,
    SkillMoveRequest,
    SkillResponse,
    SkillUpdateRequest,
)

logger = logging.getLogger(__name__)


def _skill_to_response(skill: SkillInDB) -> SkillResponse:
    """Convert SkillInDB to SkillResponse."""
    return SkillResponse(
        id=str(skill.id),
        category_id=skill.category_id,
        name=skill.name,
        index=skill.index,
        priority=skill.priority,
        difficulty=skill.difficulty,
        estimated_hours=skill.estimated_hours,
        created_at=skill.created_at,
        updated_at=skill.updated_at,
    )


async def _category_to_response(
    cat: CategoryInDB, category_repo: CategoryRepository
) -> CategoryResponse:
    """Convert CategoryInDB to CategoryResponse with nested skills."""
    skills = await category_repo.find_skills_by_category(str(cat.id))
    return CategoryResponse(
        id=str(cat.id),
        name=cat.name,
        icon=cat.icon,
        skills=[_skill_to_response(s) for s in skills],
        created_at=cat.created_at,
        updated_at=cat.updated_at,
    )


class CategoryService:
    """Business logic for category and skill management."""

    def __init__(
        self,
        category_repo: CategoryRepository,
        progress_repo: ProgressRepository,
        comment_repo: CommentRepository,
    ) -> None:
        self._category_repo = category_repo
        self._progress_repo = progress_repo
        self._comment_repo = comment_repo

    async def get_all(self, user_id: str) -> list[CategoryResponse]:
        """Get all categories for a user.

        Args:
            user_id: The owner's user ID.

        Returns:
            List of CategoryResponse.
        """
        categories = await self._category_repo.find_all_by_user(user_id)
        return [
            await _category_to_response(c, self._category_repo)
            for c in categories
        ]

    async def get_by_id(self, category_id: str) -> CategoryResponse:
        """Get a single category by ID.

        Args:
            category_id: The category ID.

        Returns:
            CategoryResponse.

        Raises:
            CategoryNotFoundError: If the category doesn't exist.
        """
        category = await self._category_repo.find_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(f"Category {category_id} not found")
        return await _category_to_response(category, self._category_repo)

    async def create(
        self, user_id: str, payload: CategoryCreateRequest
    ) -> CategoryResponse:
        """Create a new category.

        Args:
            user_id: The owner's user ID.
            payload: Category creation data.

        Returns:
            CategoryResponse for the created category.
        """
        category = CategoryInDB(
            user_id=user_id,
            name=payload.name,
            icon=payload.icon,
        )
        existing = await self._category_repo.find_by_name_and_user(
            payload.name, user_id
        )
        if existing is not None:
            raise DuplicateError(err.ERR_CATEGORY_DUPLICATE)
        created = await self._category_repo.create(category)
        logger.info(log.LOG_CATEGORY_CREATED, created.id)
        return await _category_to_response(created, self._category_repo)

    async def update(
        self, category_id: str, payload: CategoryUpdateRequest
    ) -> CategoryResponse:
        """Update a category's fields.

        Args:
            category_id: The category ID.
            payload: Fields to update.

        Returns:
            Updated CategoryResponse.

        Raises:
            CategoryNotFoundError: If the category doesn't exist.
        """
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(category_id)

        category = await self._category_repo.update(category_id, update_data)
        if category is None:
            raise CategoryNotFoundError(f"Category {category_id} not found")
        logger.info(log.LOG_CATEGORY_UPDATED, category_id)
        return await _category_to_response(category, self._category_repo)

    async def delete(self, category_id: str) -> None:
        """Delete a category and cascade delete all related data.

        Args:
            category_id: The category ID.

        Raises:
            CategoryNotFoundError: If the category doesn't exist.
        """
        category = await self._category_repo.find_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(f"Category {category_id} not found")

        skills = await self._category_repo.find_skills_by_category(category_id)
        skill_ids = [str(s.id) for s in skills]

        if skill_ids:
            await self._progress_repo.delete_many(skill_ids)
            for sid in skill_ids:
                await self._comment_repo.delete_by_skill_id(sid)
            for skill in skills:
                await self._category_repo.delete_skill(str(skill.id))

        await self._category_repo.delete(category_id)
        logger.info(log.LOG_CATEGORY_DELETED, category_id)

    async def add_skill(
        self, category_id: str, payload: SkillCreateRequest
    ) -> SkillResponse:
        """Add a new skill to a category.

        Args:
            category_id: Parent category ID.
            payload: Skill creation data.

        Returns:
            SkillResponse for the created skill.

        Raises:
            CategoryNotFoundError: If the category doesn't exist.
        """
        category = await self._category_repo.find_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(f"Category {category_id} not found")

        # Auto-assign next index if not provided
        skills = await self._category_repo.find_skills_by_category(category_id)
        next_index = payload.index if payload.index else (
            max((s.index for s in skills), default=-1) + 1
        )

        skill = SkillInDB(
            category_id=category_id,
            name=payload.name,
            index=next_index,
            priority=payload.priority,
            difficulty=payload.difficulty,
            estimated_hours=payload.estimated_hours,
        )
        existing = await self._category_repo.find_skill_by_name_and_category(
            payload.name, category_id
        )
        if existing is not None:
            raise DuplicateError(err.ERR_SKILL_DUPLICATE)
        await self._category_repo.add_skill(category_id, skill)
        logger.info(log.LOG_SKILL_ADDED, skill.id)
        return _skill_to_response(skill)

    async def update_skill(
        self, skill_id: str, payload: SkillUpdateRequest
    ) -> SkillResponse:
        """Update a skill's fields.

        Args:
            skill_id: The skill ID.
            payload: Fields to update.

        Returns:
            Updated SkillResponse.

        Raises:
            SkillNotFoundError: If the skill doesn't exist.
        """
        skill = await self._category_repo.find_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError(f"Skill {skill_id} not found")

        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            return _skill_to_response(skill)

        updated = await self._category_repo.update_skill(skill_id, update_data)
        if updated is None:
            raise SkillNotFoundError(f"Skill {skill_id} not found")

        logger.info(log.LOG_SKILL_UPDATED, skill_id)
        return _skill_to_response(updated)

    async def get_skill(self, skill_id: str) -> SkillResponse:
        """Get a single skill by ID.

        Args:
            skill_id: The skill ID.

        Returns:
            SkillResponse.

        Raises:
            SkillNotFoundError: If the skill doesn't exist.
        """
        skill = await self._category_repo.find_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError(f"Skill {skill_id} not found")
        return _skill_to_response(skill)

    async def move_skill(
        self, skill_id: str, payload: SkillMoveRequest
    ) -> dict:
        """Move a skill up or down in display order within its category.

        Swaps the `index` value with the adjacent skill. Idempotent — if the
        skill is already at the boundary (first or last), no changes are made.

        Args:
            skill_id: The skill to move.
            payload: Direction — "up" or "down".

        Returns:
            Dict with message indicating success or no-op.

        Raises:
            SkillNotFoundError: If the skill doesn't exist.
        """
        skill = await self._category_repo.find_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError(f"Skill {skill_id} not found")

        target_index = skill.index - 1 if payload.direction == "up" else skill.index + 1

        # Find the adjacent skill to swap with
        adjacent = await self._category_repo.find_skill_by_index_and_category(
            target_index, skill.category_id
        )
        if adjacent is None:
            return {"message": "No changes made."}

        # Atomically swap indices
        swapped = await self._category_repo.swap_skill_indices(
            skill_a_id=skill.id,
            skill_b_id=adjacent.id,
            index_a=skill.index,
            index_b=adjacent.index,
        )
        if not swapped:
            return {"message": "No changes made."}

        logger.info(
            "Skill moved",
            extra={"skill_id": skill_id, "direction": payload.direction},
        )
        return {"message": "Skill moved successfully."}

    async def delete_skill(self, skill_id: str) -> None:
        """Delete a skill and cascade delete its progress and comments.

        Args:
            skill_id: The skill ID.

        Raises:
            SkillNotFoundError: If the skill doesn't exist.
        """
        skill = await self._category_repo.find_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError(f"Skill {skill_id} not found")

        await self._progress_repo.delete_by_skill_id(skill_id)
        await self._comment_repo.delete_by_skill_id(skill_id)
        await self._category_repo.delete_skill(skill_id)

        logger.info(log.LOG_SKILL_DELETED, skill_id)
