"""User repository — Beanie async data access."""

import logging

from app.models.user import User

logger = logging.getLogger(__name__)


class UserRepository:
    """Data access layer for user documents."""

    async def find_by_id(self, user_id: str) -> User | None:
        """Find a user by ID."""
        return await User.get(user_id)

    async def find_by_email(self, email: str) -> User | None:
        """Find a user by email (case-insensitive)."""
        return await User.find_one(User.email == email.lower())

    async def create(self, user: User) -> User:
        """Insert a new user document."""
        await user.create()
        logger.info("User created", extra={"user_id": str(user.id)})
        return user

    async def update(self, user_id: str, update_data: dict) -> User | None:
        """Update fields of an existing user."""
        user = await self.find_by_id(user_id)
        if user is None:
            return None
        for key, value in update_data.items():
            setattr(user, key, value)
        await user.save()
        return user

    async def delete(self, user_id: str) -> bool:
        """Remove a user document."""
        user = await self.find_by_id(user_id)
        if user is None:
            return False
        await user.delete()
        logger.info("User deleted", extra={"user_id": user_id})
        return True
