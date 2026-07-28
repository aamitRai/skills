"""Quote repository — Beanie async data access."""

import logging
import random

from app.models.quote import Quote

logger = logging.getLogger(__name__)


class QuoteRepository:
    """Data access layer for quote documents."""

    async def find_all(self) -> list[Quote]:
        """Find all quote documents."""
        return await Quote.find_all().to_list()

    async def find_random(self) -> Quote | None:
        """Find a random quote."""
        all_quotes = await self.find_all()
        if not all_quotes:
            return None
        return random.choice(all_quotes)

    async def create(self, quote: Quote) -> Quote:
        """Insert a new quote document."""
        await quote.create()
        logger.info("Quote created", extra={"quote_id": str(quote.id)})
        return quote

    async def bulk_insert(self, quotes: list[Quote]) -> int:
        """Insert multiple quotes in a single operation."""
        if not quotes:
            return 0
        await Quote.insert_many(quotes)
        logger.info("Quotes bulk inserted", extra={"count": len(quotes)})
        return len(quotes)
