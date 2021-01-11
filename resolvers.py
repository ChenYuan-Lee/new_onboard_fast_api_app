from typing import List

from ariadne import QueryType

from Validators.ranked_search_result_input_validator import RankedSearchResultInputValidator
from Validators.dates_and_price_checkinput_validator import DatesAndPriceCheckInputValidator
from Helpers.get_results_from_criteria_and_data import GetResultsFromSearchCriteriaAndData
from graphql_objects import DatesCheck
from mock_data import data

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
        id_houses_dict = {}
        for listing_id in validated_search_criteria.listing_ids:
            id_houses_dict[listing_id] = data[listing_id]
        return GetResultsFromSearchCriteriaAndData.get_data_check_results(validated_search_criteria, id_houses_dict)

    @staticmethod
    @query.field("ranked_search_results")
    def get_ranked_search_results(
            _,
            info,
            **search_criteria
    ) -> List[DatesCheck]:
        validated_search_criteria = RankedSearchResultInputValidator(**search_criteria)
        print(type(validated_search_criteria))
        return GetResultsFromSearchCriteriaAndData.get_data_check_results(validated_search_criteria, data)
