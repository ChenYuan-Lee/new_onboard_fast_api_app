from dataclasses import dataclass
from typing import Any

from constants import PRICE_BREAKDOWNS_LOADER_NAME


@dataclass
class Listing:
    listing_id: int
    bedrooms: int
    bathrooms: float

    async def get_price_breakdown(self, info: Any):
        price_breakdown_loader = info.context[PRICE_BREAKDOWNS_LOADER_NAME]
        print(type(price_breakdown_loader))
        return await price_breakdown_loader.load(self.listing_id)
