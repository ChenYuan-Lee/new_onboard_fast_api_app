from typing import List

from ariadne import QueryType

from graphql_objects import DatesCheck
from mock_data import data
from validators import DatesAndPriceCheckInputValidator

query = QueryType()


class QueryResolvers:

    @staticmethod
    @query.field("dates_and_price_check")
    def get_dates_and_price_check(
            _,
            info,
            **search_criteria
    ) -> List[DatesCheck]:
        validated_search_criteria = DatesAndPriceCheckInputValidator(**search_criteria)
        results_list = []
        for listing_id in validated_search_criteria.listing_ids:
            listing = data[listing_id]
            dates_check = DatesCheck(
                listing_id=listing.listing_id
            )
            results_list.append(dates_check)
        return results_list
