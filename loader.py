from typing import List

from aiodataloader import DataLoader

from data_models import Listing
from graphql_objects import PriceBreakdown
from mock_data import ListingsDataDB, PricesDataDB


class ListingsLoader(DataLoader):
    def __init__(self):
        super().__init__()

    @staticmethod
    async def batch_load_fn(listing_ids: List[int]) -> List[Listing]:
        list_of_listings_data = ListingsDataDB.get_listings_data_from_db(listing_ids)
        return [Listing(**listing_data) for listing_data in list_of_listings_data]


class PriceBreakdownsLoader(DataLoader):
    def __init__(self):
        super().__init__()

    @staticmethod
    async def batch_load_fn(listing_ids: List[int]) -> List[PriceBreakdown]:
        list_of_prices = PricesDataDB.get_prices_data_from_db(listing_ids)
        return [PriceBreakdown(dollars=price) for price in list_of_prices]
