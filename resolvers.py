from typing import List, Union

from ariadne import QueryType, UnionType

from validators.ranked_search_result_input_validator import RankedSearchResultInputValidator
from validators.dates_and_price_checkinput_validator import DatesAndPriceCheckInputValidator
from helpers.get_results_from_criteria_and_data import DatesCheckGetter
from graphql_objects import DatesCheck, Error, ListingUnsupportedError, GenericError
from mock_data import data

query = QueryType()


class QueryResolvers:

    @staticmethod
    @query.field("dates_and_price_check")
    def get_dates_and_price_check(
            _,
            info,
            **search_criteria
    ) -> List[Union[DatesCheck, Error]]:
        try:
            validated_search_criteria = DatesAndPriceCheckInputValidator(**search_criteria)
            id_houses_dict = {}
            unsupported_listing = []
            for listing_id in validated_search_criteria.listing_ids:
                if listing_id in data.keys():
                    id_houses_dict[listing_id] = data[listing_id]
                else:
                    unsupported_listing.append(listing_id)
            if len(unsupported_listing) != 0:
                return [ListingUnsupportedError("Few listings are not out of scope. Please check the listings provided",
                                                unsupported_listing
                                                )
                        ]
            return DatesCheckGetter.get_date_check_results(validated_search_criteria, id_houses_dict)
        except:
            return [GenericError(f"Something seems to have gone wrong. Please check the input field values")]

    @staticmethod
    @query.field("ranked_search_results")
    def get_ranked_search_results(
            _,
            info,
            **search_criteria
    ) -> List[Union[DatesCheck, Error]]:
        try:
            validated_search_criteria = RankedSearchResultInputValidator(**search_criteria)
            return DatesCheckGetter.get_date_check_results(validated_search_criteria, data)
        except:
            return [GenericError(f"Something seems to have gone wrong. Please check the input field values")]
