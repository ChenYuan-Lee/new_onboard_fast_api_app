from datetime import date, timedelta
from typing import List, Dict

from Validators.checkin_checkout_validator import CheckinCheckoutValidator
from graphql_objects import DatesCheck
from mock_data import House


class GetResultsFromSearchCriteriaAndData:

    @staticmethod
    def get_data_check_results(
            validated_search_criteria: CheckinCheckoutValidator,
            id_to_houses_dict: Dict[id, House]
    ) -> List[DatesCheck]:
        """
        Parent function to get the Date Availability when under different conditions - when Checkin and Checkout are
        provided or skipped
        @param validated_search_criteria: Parsed validator to run the logic on
        @type validated_search_criteria: CheckinCheckoutValidator
        @param id_to_houses_dict: Listing IDs to Houses Dictionary
        @type id_to_houses_dict: Dict{id, House}
        @return: Returns the list of DatesCheck objects which show whether a house is available or not given the search
        criteria
        @rtype: List[DatesCheck]
        """
        results_list: List[DatesCheck] = []
        desired_checkin = validated_search_criteria.desired_checkin
        desired_checkout = validated_search_criteria.desired_checkout
        for house in id_to_houses_dict.values():
            if desired_checkin is None and desired_checkout is None:
                data_check = GetResultsFromSearchCriteriaAndData.update_data_check_when_null_checkin_checkout(
                    house=house
                )
            elif desired_checkout is None:
                data_check = GetResultsFromSearchCriteriaAndData.update_data_check_when_only_checkin_provided(
                    desired_checkin=desired_checkin,
                    house=house,
                )
            else:
                data_check = GetResultsFromSearchCriteriaAndData.update_data_check_when_both_checkin_checkout_provided(
                    desired_checkin=desired_checkin,
                    desired_checkout=desired_checkout,
                    house=house,
                )
            results_list.append(data_check)

        return results_list

    @staticmethod
    def update_data_check_when_both_checkin_checkout_provided(
            desired_checkin: date,
            desired_checkout: date,
            house: House
    ) -> DatesCheck:
        """
        Updates the required parameters of the DatesCheck object when both checkin and checkout are provided.
        """
        is_available = False
        for date_ranges in house.available_ranges:
            if (
                    desired_checkin >= date_ranges.range_start and
                    desired_checkout <= date_ranges.range_end and
                    int((desired_checkout - desired_checkin).days) >= house.min_stay_nights
            ):
                is_available = True
                break

        return DatesCheck(
            listing_id=house.listing_id,
            is_available=is_available,
            checkin_date=desired_checkin,
            checkout_date=desired_checkout
        )

    @staticmethod
    def update_data_check_when_only_checkin_provided(
            desired_checkin: date,
            house: House
    ) -> DatesCheck:
        """
        Updates the required parameters of the DatesCheck Object when only checkin is provided
        """
        checkin_date = desired_checkin
        checkout_date = None
        is_available = False
        for date_ranges in house.available_ranges:
            if (
                    desired_checkin >= date_ranges.range_start and
                    desired_checkin + timedelta(days=house.min_stay_nights) <= date_ranges.range_end
            ):
                checkout_date = desired_checkin + timedelta(days=house.min_stay_nights)
                is_available = True
                break
            elif desired_checkin > date_ranges.range_start:
                continue
            else:
                is_available = True
                checkin_date = date_ranges.range_start
                checkout_date = date_ranges.range_start + timedelta(days=house.min_stay_nights)
                break

        return DatesCheck(
            listing_id=house.listing_id,
            is_available=is_available,
            checkin_date=checkin_date,
            checkout_date=checkout_date

        )

    @staticmethod
    def update_data_check_when_null_checkin_checkout(
            house: House
    ) -> DatesCheck:
        """
        Update and create the DatesCheck object when neighter checkin nor checkout is provided
        #Assumption : There is a always a house in the data with available dates
        """
        if date.today() > house.available_ranges[0].range_start:
            checkin_date = date.today()
            checkout_date = date.today() + timedelta(days=house.min_stay_nights)
        else:
            checkin_date = house.available_ranges[0].range_start
            checkout_date = house.available_ranges[0].range_start + timedelta(days=house.min_stay_nights)
        return DatesCheck(
            listing_id=house.listing_id,
            is_available=True,
            checkin_date=checkin_date,
            checkout_date=checkout_date
        )
