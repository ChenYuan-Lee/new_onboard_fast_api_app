from typing import Any

from data_models import Listing


class ListingsCheck:

    def __init__(
        self,
        listing: Listing,
    ):
        self.listing = listing
        self.listing_id = listing.listing_id
        self.bedrooms = listing.bedrooms
        self.bathrooms = listing.bathrooms

    async def price_breakdown(self, info: Any) -> float:
        return await self.listing.get_price_breakdown(info)


class PriceBreakdown:

    def __init__(self, dollars: float):
        self.dollars = dollars
