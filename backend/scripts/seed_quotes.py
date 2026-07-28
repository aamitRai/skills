"""Script to seed quotes from quotes.json into MongoDB using Beanie."""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.quote import Quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_quotes():
    # Initialize Beanie
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
    )
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[Quote],
    )
    logger.info("Connected to MongoDB: %s", settings.MONGODB_DB_NAME)

    # Load quotes from JSON file
    quotes_file = Path(__file__).parent.parent / "app" / "data" / "quotes.json"
    with open(quotes_file, "r") as f:
        raw_quotes = json.load(f)

    # Check if quotes already exist
    existing_count = await Quote.count()
    if existing_count > 0:
        logger.warning(
            "Quotes collection already has %d documents. Skipping seed.",
            existing_count,
        )
        client.close()
        return

    # Map JSON fields to Beanie model fields
    # JSON: { "id": 1, "category": "Mindset", "quote": "..." }
    # Model: { "text": str, "author": str }
    quotes = [
        Quote(
            text=item["quote"],
            author="",
        )
        for item in raw_quotes
    ]

    # Bulk insert
    await Quote.insert_many(quotes)
    logger.info("Seeded %d quotes into the database", len(quotes))

    client.close()


if __name__ == "__main__":
    asyncio.run(seed_quotes())
