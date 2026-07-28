"""
MongoDB async connection management using Beanie ODM.

Initializes Beanie document store and provides dependency injection.
"""

import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import certifi

from app.core.config import settings
from app.models.user import User
from app.models.category import Category, Skill
from app.models.progress import SkillProgress
from app.models.comment import Comment
from app.models.quote import Quote
from app.models.settings import UserSettings

logger = logging.getLogger(__name__)

_client: AsyncIOMotorClient | None = None


async def init_db() -> None:
    """
    Initialize MongoDB client and register Beanie document models.

    Call this once during application startup.
    """
    global _client
    _client = AsyncIOMotorClient(
        settings.MONGODB_URI,
            tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000,
    )
    await init_beanie(
        database=_client[settings.MONGODB_DB_NAME],
        document_models=[
            User,
            Category,
            Skill,
            SkillProgress,
            Comment,
            Quote,
            UserSettings,
        ],
    )
    logger.info(
        "Beanie initialized",
        extra={"db_name": settings.MONGODB_DB_NAME},
    )


async def close_db() -> None:
    """Close the MongoDB client connection."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
        logger.info("MongoDB client closed")
