from datetime import datetime
from typing import List

from ariadne import QueryType

from graphql_objects import DatesCheck
from mock_data import data, House
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
            listing: House = data[listing_id]
            dates = listing.available_ranges
            available_date = datetime.today().date()
            for date in dates:
                if date.range_start > validated_search_criteria.desired_checkin:
                    available_date = date.range_start
                    break
            dates_check = DatesCheck(
                listing_id=listing.listing_id,
                next_available_checkin_date=available_date
            )
            results_list.append(dates_check)
        return results_list
