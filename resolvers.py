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
        results_list:List[DatesCheck] = []
        for listing_id in validated_search_criteria.listing_ids:
            #Assumption that the data is already present
            listing: House = data[listing_id]
            dates = listing.available_ranges
            available_date = date.today()
            add_date_flag = 0
            for range_date in dates:
                if range_date.range_start > validated_search_criteria.desired_checkin:
                    available_date = range_date.range_start
                    add_date_flag = 1
                    dates_check = DatesCheck(
                        listing_id=listing.listing_id,
                        is_available=False,
                        checkin_date=validated_search_criteria.desired_checkin,
                        checkout_date=validated_search_criteria.desired_checkout
                    )
                    results_list.append(dates_check)
                    break
            if not add_date_flag:
                dates_check = DatesCheck(
                    listing_id=listing.listing_id,
                    is_available=False,
                    checkin_date= validated_search_criteria.desired_checkin,
                    checkout_date= validated_search_criteria.desired_checkout
                )
                results_list.append(dates_check)
        return results_list

    @staticmethod
    @query.field("ranked_search_results")
    def get_ranked_search_results(
            _,
            info,
            **search_criteria
    ) -> List[DatesCheck]:
        validated_search_criteria = RankedSearchResultInputValidator(**search_criteria)
        results_list:List[DatesCheck] = []
        checkin_Desired = validated_search_criteria.desired_checkin
        checkout_Desired = validated_search_criteria.desired_checkout
        if checkin_Desired is None and checkout_Desired is None:
            for house in data.values():
                data_check = DatesCheck(house.listing_id, True, house.available_ranges[0].range_start, house.available_ranges[0].range_start + timedelta(days=house.min_stay_nights))
                results_list.append(data_check)

        elif checkout_Desired is None:
            for house in data.values():
                for range in house.available_ranges:
                    if checkin_Desired > range.range_start:
                        continue
                    else:
                        data_check = DatesCheck(house.listing_id, True, range.range_start, range.range_start + timedelta(days=house.min_stay_nights))
                        results_list.append(data_check)
                        break

                if len(results_list) == 0:
                   results_list.append(DatesCheck(house.listing_id, False, checkin_Desired, checkout_Desired))


        else:
            for house in data.values():
                for range in house.available_ranges:
                    if checkin_Desired >= range.range_start and checkout_Desired <= range.range_end and int((checkout_Desired - checkin_Desired).days) > house.min_stay_nights :
                        data_check = DatesCheck(house.listing_id, True, checkin_Desired, checkout_Desired)
                        results_list.append(data_check)
                        break
                if len(results_list) == 0:
                   results_list.append(DatesCheck(house.listing_id, False, checkin_Desired, checkout_Desired))

        return results_list






