from datetime import date
from typing import Optional

from pydantic import validator
from pydantic.main import BaseModel


class CheckinCheckoutValidator(BaseModel):
    desired_checkin: Optional[date]
    desired_checkout: Optional[date]

    @validator('desired_checkin')
    def date_must_be_greater_than_today(
            cls,
            desired_checkin: Optional[date]
    ) -> Optional[date]:
        """
        Check for date to be greater than today
        """
        if desired_checkin < desired_checkin.today():
            raise ValueError(f'Date must be after today{desired_checkin.today()}')
        return desired_checkin

    @validator('desired_checkout')
    def checkout_date_present(
            cls,
            desired_checkout: Optional[date],
            values
    ) -> Optional[date]:
        """
        Check if desired checkout is present without checkin being present. If so Raise ValueError
        """
        if desired_checkout is not None and values.get('desired_checkin') is None:
            raise ValueError("Checkout date exists without checkin Date")
        return desired_checkout

    @validator('desired_checkout')
    def checkin_date_before_checkout_date(
            cls,
            desired_checkout: Optional[date],
            values
    ) -> Optional[date]:
        """
        Does a check to see if check in date is before the checkout date
        """
        if 'desired_checkin' in values and desired_checkout <= values['desired_checkin']:
            raise ValueError("Checkout date before Checkin Date")
        return desired_checkout
