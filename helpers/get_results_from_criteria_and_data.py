from datetime import date, timedelta
from typing import List, Dict

from validators.checkin_checkout_validator import CheckinCheckoutValidator
from graphql_objects import DatesCheck
from mock_data import House


class DatesCheckGetter:

    @staticmethod
    def get_date_check_results(
            validated_search_criteria: CheckinCheckoutValidator,
            id_to_houses_dict: Dict[id, House]
    ) -> List[DatesCheck]:
        """
        Parent function to get the Date Availability under different conditions - when Checkin and Checkout are
        provided or skipped
        """
        results_list: List[DatesCheck] = []
        for house in id_to_houses_dict.values():
            date_check = DatesCheckGetter.get_date_check_result_for_house(validated_search_criteria, house)
            results_list.append(date_check)
        return results_list

    @staticmethod
    def get_date_check_result_for_house(
            validated_search_criteria: CheckinCheckoutValidator,
            house: House
    ) -> DatesCheck:
        desired_checkin = validated_search_criteria.desired_checkin
        desired_checkout = validated_search_criteria.desired_checkout
        if desired_checkin is None and desired_checkout is None:
            date_check = DatesCheckGetter.update_date_check_when_null_checkin_checkout(
                house=house
            )
        elif desired_checkout is None:
            date_check = DatesCheckGetter.update_date_check_when_only_checkin_provided(
                desired_checkin=desired_checkin,
                house=house,
            )
        else:
            date_check = DatesCheckGetter.update_date_check_when_both_checkin_checkout_provided(
                desired_checkin=desired_checkin,
                desired_checkout=desired_checkout,
                house=house,
            )
        return date_check

    @staticmethod
    def update_date_check_when_both_checkin_checkout_provided(
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
    def update_date_check_when_only_checkin_provided(
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
    def update_date_check_when_null_checkin_checkout(
            house: House
    ) -> DatesCheck:
        """
        Update and create the DatesCheck object when neighter checkin nor checkout is provided
        #Assumption : There is a always a house in the data with available dates and the available dates don't have
        expired ranges.
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
