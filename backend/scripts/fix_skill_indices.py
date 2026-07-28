"""Script to fix skill indices — assigns sequential indices per category."""

import asyncio
import logging
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.category import Category, Skill

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fix_skill_indices():
    # Initialize Beanie
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
    )
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[Category, Skill],
    )
    logger.info("Connected to MongoDB: %s", settings.MONGODB_DB_NAME)

    # Get all categories
    categories = await Category.find_all().to_list()
    total_fixed = 0

    for category in categories:
        skills = await Skill.find(
            Skill.category_id == str(category.id)
        ).sort(Skill.created_at).to_list()

        for i, skill in enumerate(skills):
            if skill.index != i:
                skill.index = i
                await skill.save()
                total_fixed += 1
                logger.info(
                    "Updated %s in %s → index=%d",
                    skill.name, category.name, i,
                )

    logger.info("Done. Fixed %d skills across %d categories", total_fixed, len(categories))
    client.close()


if __name__ == "__main__":
    asyncio.run(fix_skill_indices())
