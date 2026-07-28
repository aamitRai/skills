"""Category repository — Beanie async data access."""

import logging
import re

from app.models.category import Category, Skill

logger = logging.getLogger(__name__)


class CategoryRepository:
    """Data access layer for category and skill documents."""

    async def find_all_by_user(self, user_id: str) -> list[Category]:
        """Find all categories for a user."""
        cursor = Category.find(Category.user_id == user_id)
        return await cursor.to_list()

    async def find_by_id(self, category_id: str) -> Category | None:
        """Find a single category by ID."""
        return await Category.get(category_id)

    async def find_by_name_and_user(
        self, name: str, user_id: str
    ) -> Category | None:
        """Find a category by name (case-insensitive) for a specific user."""
        return await Category.find_one({
            "user_id": user_id,
            "name": {"$regex": re.escape(name), "$options": "i"},
        })

    async def create(self, category: Category) -> Category:
        """Insert a new category document."""
        await category.create()
        logger.info("Category created", extra={"category_id": str(category.id)})
        return category

    async def update(self, category_id: str, update_data: dict) -> Category | None:
        """Update fields of an existing category."""
        category = await self.find_by_id(category_id)
        if category is None:
            return None
        for key, value in update_data.items():
            setattr(category, key, value)
        await category.save()
        return category

    async def delete(self, category_id: str) -> bool:
        """Remove a category document."""
        category = await self.find_by_id(category_id)
        if category is None:
            return False
        await category.delete()
        logger.info("Category deleted", extra={"category_id": category_id})
        return True

    async def add_skill(self, category_id: str, skill: Skill) -> Skill:
        """Add a new skill document linked to a category."""
        await skill.create()
        return skill

    async def update_skill(
        self, skill_id: str, update_data: dict
    ) -> Skill | None:
        """Update a skill document."""
        skill = await Skill.get(skill_id)
        if skill is None:
            return None
        for key, value in update_data.items():
            setattr(skill, key, value)
        await skill.save()
        return skill

    async def delete_skill(self, skill_id: str) -> bool:
        """Remove a skill document."""
        skill = await Skill.get(skill_id)
        if skill is None:
            return False
        await skill.delete()
        return True

    async def find_skills_by_category(self, category_id: str) -> list[Skill]:
        """Find all skills belonging to a category, sorted by index."""
        cursor = Skill.find(Skill.category_id == category_id).sort(Skill.index)
        return await cursor.to_list()

    async def find_skill_by_id(self, skill_id: str) -> Skill | None:
        """Find a skill by ID."""
        return await Skill.get(skill_id)

    async def find_skill_by_name_and_category(
        self, name: str, category_id: str
    ) -> Skill | None:
        """Find a skill by name (case-insensitive) within a category."""
        return await Skill.find_one({
            "category_id": category_id,
            "name": {"$regex": re.escape(name), "$options": "i"},
        })

    async def find_skill_by_index_and_category(
        self, index: int, category_id: str
    ) -> Skill | None:
        """Find a skill by index position within a category."""
        return await Skill.find_one({
            "category_id": category_id,
            "index": index,
        })

    async def swap_skill_indices(
        self, skill_a_id: str, skill_b_id: str, index_a: int, index_b: int
    ) -> bool:
        """Swap index values of two skills."""
        skill_a = await Skill.get(skill_a_id)
        skill_b = await Skill.get(skill_b_id)
        if skill_a is None or skill_b is None:
            return False

        skill_a.index = index_b
        skill_b.index = index_a
        await skill_a.save()
        await skill_b.save()
        return True

    async def find_category_by_skill_id(self, skill_id: str) -> Category | None:
        """Find the category that contains a given skill."""
        skill = await Skill.get(skill_id)
        if skill is None:
            return None
        return await Category.get(skill.category_id)

    async def update_skill_in_category(
        self, category_id: str, skill_id: str, update_data: dict
    ) -> Category | None:
        """Update a skill within its category document and return the category."""
        category = await self.find_by_id(category_id)
        if category is None:
            return None
        skill = await Skill.get(skill_id)
        if skill is None:
            return None
        for key, value in update_data.items():
            setattr(skill, key, value)
        await skill.save()
        return category

    async def delete_skill_from_category(
        self, category_id: str, skill_id: str
    ) -> bool:
        """Delete a skill from its category."""
        return await self.delete_skill(skill_id)
