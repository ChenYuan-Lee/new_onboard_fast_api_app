from dataclasses import dataclass
from typing import Any

from constants import PRICE_BREAKDOWNS_LOADER_NAME


@dataclass
class Listing:
    listing_id: int
    bedrooms: int
    bathrooms: float

    async def get_price_breakdown(self, info: Any):
        print(f"Listing {self.listing_id} is calling PriceBreakdown.load function")
        return await info.context[PRICE_BREAKDOWNS_LOADER_NAME].load(self)

    def __hash__(self):
        """
        Observation for deduplication behaviour of aiodataloader.DataLoader: it first compares the outputs of the
        __hash__ function – if both objects gives the same __hash__ output, it then uses the __eq__ function
        """
        hash_output = self.listing_id
        print(f"Listing {self.listing_id}'s __hash__ function called | output: {hash_output}")
        return hash_output

    def __eq__(self, other):
        equality = self.listing_id == other.listing_id
        print(f"Listing {self.listing_id}'s __eq__ function called to compare against listing {other.listing_id} | output: {equality}")
        return equality
