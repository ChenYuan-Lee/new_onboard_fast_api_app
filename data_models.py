from dataclasses import dataclass
from typing import Any

from constants import PRICE_BREAKDOWNS_LOADER_NAME


@dataclass
class Listing:
    listing_id: int
    bedrooms: int
    bathrooms: float

    async def get_price_breakdown(self, info: Any):
        print(f"Obtaining PriceBreakdown for listing {self.listing_id}")
        return await info.context[PRICE_BREAKDOWNS_LOADER_NAME].load(self)

    def __hash__(self):
        return self.listing_id

