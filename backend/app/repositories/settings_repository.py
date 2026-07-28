"""Settings repository — Beanie async data access."""

import logging

from app.models.settings import UserSettings

logger = logging.getLogger(__name__)


class SettingsRepository:
    """Data access layer for settings documents."""

    async def find_by_user_id(self, user_id: str) -> UserSettings | None:
        """Find settings for a specific user."""
        return await UserSettings.find_one(UserSettings.user_id == user_id)

    async def upsert(
        self, user_id: str, theme: str | None = None, remember: bool | None = None
    ) -> UserSettings:
        """Insert or update settings for a user."""
        settings = await self.find_by_user_id(user_id)
        if settings is not None:
            if theme is not None:
                settings.theme = theme
            if remember is not None:
                settings.remember = remember
            await settings.save()
        else:
            settings = UserSettings(
                user_id=user_id,
                theme=theme or "light",
                remember=remember if remember is not None else False,
            )
            await settings.create()
        logger.info("Settings upserted", extra={"user_id": user_id})
        return settings
