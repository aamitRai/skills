"""Script to create an admin user in MongoDB using Beanie."""

import asyncio
import logging
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_admin_user():
    # Initialize Beanie (same as the app does in database.py)
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
    )
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[User],
    )
    logger.info("Connected to MongoDB: %s", settings.MONGODB_DB_NAME)

    # Check if user already exists
    existing = await User.find_one(User.email == "amitrai8602@gmail.com")
    if existing:
        logger.info("User already exists: %s", existing.email)
        client.close()
        return

    # Create admin user using Beanie model
    user = User(
        email="amitrai8602@gmail.com",
        name="Amit Rai",
        title="Admin",
        hashed_password=hash_password("Ideapad@123"),
        avatar_url=None,
    )
    await user.create()
    logger.info("Admin user created: %s (id: %s)", user.email, user.id)

    client.close()


if __name__ == "__main__":
    asyncio.run(create_admin_user())
