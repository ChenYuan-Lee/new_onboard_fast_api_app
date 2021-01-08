from datetime import date, timedelta
from typing import List

from graphql_objects import DatesCheck


class GetResultsFromSearchCriteriaAndData():

    @staticmethod
    def get_data_check_results(validated_search_criteria, id_houses_dict: dict) -> List[DatesCheck]:
        results_list: List[DatesCheck] = []
        checkin_desired = validated_search_criteria.desired_checkin
        checkout_desired = validated_search_criteria.desired_checkout
        for house in id_houses_dict.values():
            data_check = DatesCheck(listing_id=house.listing_id,
                                    is_available=True,
                                    checkin_date=checkin_desired,
                                    checkout_date=checkout_desired)
            if checkin_desired is None and checkout_desired is None:
                data_check = GetResultsFromSearchCriteriaAndData.update_data_check_when_null_checkin_checkout(
                    data_check= data_check,
                    house= house)
            elif checkout_desired is None:
                data_check = GetResultsFromSearchCriteriaAndData.update_data_check_when_only_non_null_checkin(
                    checkin_desired=checkin_desired,
                    data_check=data_check,
                    house=house,
                )
            else:
                data_check = GetResultsFromSearchCriteriaAndData.update_data_check_when_non_null_checkin_checkout(
                    checkin_desired=checkin_desired,
                    checkout_desired=checkout_desired,
                    data_check=data_check,
                    house=house,
                    )
            results_list.append(data_check)

            if len(results_list) == 0:
                data_check.is_available = False
        return results_list

    @staticmethod
    def update_data_check_when_non_null_checkin_checkout(checkin_desired, checkout_desired, data_check, house):
        for date_ranges in house.available_ranges:
            if checkin_desired >= date_ranges.range_start and checkout_desired <= date_ranges.range_end and int(
                    (checkout_desired - checkin_desired).days) > house.min_stay_nights:
                data_check = data_check
                return data_check
        data_check.is_available = False
        return data_check

    @staticmethod
    def update_data_check_when_only_non_null_checkin(checkin_desired, data_check, house):
        for date_ranges in house.available_ranges:
            if checkin_desired > date_ranges.range_start and checkin_desired + timedelta(
                    days=house.min_stay_nights) < date_ranges.range_end:
                data_check.checkin_date = checkin_desired
                data_check.checkout_date = checkin_desired + timedelta(days=house.min_stay_nights)
                return data_check
            if checkin_desired > date_ranges.range_start:
                continue
            else:
                data_check.checkin_date = date_ranges.range_start
                data_check.checkout_date = date_ranges.range_start + timedelta(days=house.min_stay_nights)
                return data_check
        data_check.is_available = False
        return data_check

    @staticmethod
    def update_data_check_when_null_checkin_checkout(data_check, house):
        if date.today() > house.available_ranges[0].range_start:
            data_check.checkin_date = date.today()
            data_check.checkout_date = date.today() + timedelta(days=house.min_stay_nights)
        else:
            data_check.checkin_date = house.available_ranges[0].range_start
            data_check.checkout_date = date(
                house.available_ranges[0].range_start + timedelta(days=house.min_stay_nights))
        return data_check