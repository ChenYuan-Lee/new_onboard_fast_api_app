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
            dates_and_price_check_results = []
            for listing_id in validated_search_criteria.listing_ids:
                if listing_id in data.keys():
                    dates_and_price_check_results.append(
                        DatesCheckGetter.get_date_check_result_for_house(
                            validated_search_criteria,
                            data[listing_id]
                        )
                    )
                else:
                    dates_and_price_check_results.append(ListingUnsupportedError(f"Listing {listing_id} out of scope"))

            return dates_and_price_check_results

        except Exception as e:
            return [GenericError(f"Something seems to have gone wrong. Please check the error message {e}")]

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
        except Exception as e:
            return [GenericError(f"Something seems to have gone wrong. Please check the error message {e}")]
