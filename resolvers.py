from typing import List, Union

from ariadne import QueryType, UnionType

from validators.ranked_search_result_input_validator import RankedSearchResultInputValidator
from validators.dates_and_price_checkinput_validator import DatesAndPriceCheckInputValidator
from helpers.get_results_from_criteria_and_data import DatesCheckGetter
from graphql_objects import DatesCheck, Error
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
            for listing_id in validated_search_criteria.listing_ids:
                id_houses_dict[listing_id] = data[listing_id]
            return DatesCheckGetter.get_date_check_results(validated_search_criteria, id_houses_dict)
        except:
            return [Error(f"There is an error. Please check the fields attached")]

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
            return [Error(f"Ranked search results returned an error. Please check the fields attached")]
