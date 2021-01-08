from datetime import datetime, timedelta, date
from typing import List

from ariadne import QueryType

from Validators.RankedSearchResultInputValidator import RankedSearchResultInputValidator
from Validators.DatesAndPriceCheckInputValidator import DatesAndPriceCheckInputValidator
from graphql_objects import DatesCheck
from mock_data import data, House

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
        houses_list = {}
        for listing_id in validated_search_criteria.listing_ids:
            houses_list[listing_id] = data[listing_id]
        return QueryResolvers.getResultsList(validated_search_criteria, houses_list)

    @staticmethod
    @query.field("ranked_search_results")
    def get_ranked_search_results(
            _,
            info,
            **search_criteria
    ) -> List[DatesCheck]:
        validated_search_criteria = RankedSearchResultInputValidator(**search_criteria)
        return QueryResolvers.getResultsList(validated_search_criteria, data)

    @staticmethod
    def getResultsList(validated_search_criteria, houses_list: dict) -> List[DatesCheck]:
        results_list: List[DatesCheck] = []
        checkin_Desired = validated_search_criteria.desired_checkin
        checkout_Desired = validated_search_criteria.desired_checkout
        if checkin_Desired is None and checkout_Desired is None:
            for house in houses_list.values():
                data_check = DatesCheck(house.listing_id, True, house.available_ranges[0].range_start,
                                        house.available_ranges[0].range_start + timedelta(days=house.min_stay_nights))
                results_list.append(data_check)

        elif checkout_Desired is None:
            for house in houses_list.values():
                for range in house.available_ranges:
                    if checkin_Desired > range.range_start and checkin_Desired + timedelta(
                            days=house.min_stay_nights) < range.range_end:
                        data_check = DatesCheck(house.listing_id, True, checkin_Desired,
                                                checkin_Desired + timedelta(days=house.min_stay_nights))
                        results_list.append(data_check)
                        break

                    if checkin_Desired > range.range_start:
                        continue
                    else:
                        data_check = DatesCheck(house.listing_id, True, range.range_start,
                                                range.range_start + timedelta(days=house.min_stay_nights))
                        results_list.append(data_check)
                        break

                if len(results_list) == 0:
                    results_list.append(DatesCheck(house.listing_id, False, checkin_Desired, checkout_Desired))


        else:
            for house in houses_list.values():
                for range in house.available_ranges:
                    if checkin_Desired >= range.range_start and checkout_Desired <= range.range_end and int(
                            (checkout_Desired - checkin_Desired).days) > house.min_stay_nights:
                        data_check = DatesCheck(house.listing_id, True, checkin_Desired, checkout_Desired)
                        results_list.append(data_check)
                        break
                if len(results_list) == 0:
                    results_list.append(DatesCheck(house.listing_id, False, checkin_Desired, checkout_Desired))
        return results_list
