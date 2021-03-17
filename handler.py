import asyncio
from _asyncio import Future
from typing import Any, List

from constants import LISTINGS_LOADER_NAME
from data_models import Listing
from graphql_objects import ListingsCheck
from validators import ListingsCheckInputValidator


class Handler:
    @classmethod
    async def serve(
        cls,
        info: Any,
        search_criteria: ListingsCheckInputValidator,
    ) -> List[ListingsCheck]:
        listing_check_coroutines: List[Future] = [
            info.context[LISTINGS_LOADER_NAME].load(listing_id) for listing_id in search_criteria.listing_ids
        ]
        listings: List[Listing] = await asyncio.gather(*listing_check_coroutines)
        return [ListingsCheck(listing) for listing in listings]

        # If you use the following code instead, you will notice that the number of calls to the DB would increase from
        # 1 to N times.
        # results_list = []
        # for listing_id in search_criteria.listing_ids:
        #     listing = await info.context[LISTINGS_LOADER_NAME].load(listing_id)
        #     listing_check = ListingsCheck(listing)
        #     results_list.append(listing_check)
        # return results_list
