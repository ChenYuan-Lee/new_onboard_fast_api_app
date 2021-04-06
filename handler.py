import asyncio
from _asyncio import Future
from typing import Any, List

from constants import LISTINGS_LOADER_NAME, PRICE_BREAKDOWNS_LOADER_NAME
from data_models import Listing
from graphql_objects import ListingsCheck
from loader import PriceBreakdownsLoader, ListingsLoader, ListingsLoader2, PriceBreakdownsLoader2
from validators import ListingsCheckInputValidator


class Handler:
    @classmethod
    async def serve(
        cls,
        info: Any,
        search_criteria: ListingsCheckInputValidator,
    ) -> List[ListingsCheck]:

        search_criteria_1 = search_criteria.copy()
        search_criteria_1.listing_ids = search_criteria_1.listing_ids[:-1]
        listings_loader_1 = ListingsLoader()
        price_breakdowns_loader_1 = PriceBreakdownsLoader()

        search_criteria_2 = search_criteria.copy()
        search_criteria_2.listing_ids = search_criteria_2.listing_ids[-1:]
        listings_loader_2 = ListingsLoader2()
        price_breakdowns_loader_2 = PriceBreakdownsLoader2()

        all_search_criteria = [
            (search_criteria_1, listings_loader_1, price_breakdowns_loader_1),
            (search_criteria_2, listings_loader_2, price_breakdowns_loader_2),
        ]

        output = []
        for search_criteria, listings_loader, price_breakdowns_loader in all_search_criteria:
            info.context[LISTINGS_LOADER_NAME] = listings_loader
            info.context[PRICE_BREAKDOWNS_LOADER_NAME] = price_breakdowns_loader
            listing_check_coroutines = [
                info.context[LISTINGS_LOADER_NAME].load(listing_id) for listing_id in search_criteria.listing_ids
            ]
            listings = await asyncio.gather(*listing_check_coroutines)
            listing_checks = [ListingsCheck(listing) for listing in listings]
            output.extend(listing_checks)

        return output

        # If you use the following code instead, you will notice that the number of calls to the DB would increase from
        # 1 to N times.
        # results_list = []
        # for listing_id in search_criteria.listing_ids:
        #     listing = await info.context[LISTINGS_LOADER_NAME].load(listing_id)
        #     listing_check = ListingsCheck(listing)
        #     results_list.append(listing_check)
        # return results_list
