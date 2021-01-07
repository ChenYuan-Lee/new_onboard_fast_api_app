from datetime import date
from typing import Optional

from pydantic import validator
from pydantic.main import BaseModel
from pydantic.types import conint, conlist


class DatesAndPriceCheckInputValidator(BaseModel):
    listing_ids: conlist(conint(gt=0), min_items=1)
    desired_checkin:Optional[date]
    desired_checkout: Optional[date]

    @validator('desired_checkin')
    def date_must_be_greater_than_today(cls, date: Optional[date]) -> Optional[date]:
        """
        Checks date is greater than today
        @param date: Desired Checkin Date
        @type date: Optional[date]
        @return: Optional[date]
        """
        if date < date.today():
            raise ValueError(f'Date must be after today{date.today()}')
        return date

    @validator('desired_checkout')
    def checkin_date_before_checkout_date(cls, checkout_date: Optional[date], values, **kwargs) -> Optional[date]:
        print(values)
        if checkout_date < values['desired_checkin']:
            raise ValueError("Checkout date before Checkin Date")
        return checkout_date

    @validator('desired_checkout')
    def checkout_date_present(cls, checkout_date: Optional[date], values, **kwargs) -> Optional[date]:
        if checkout_date != None and values['desired_checkin'] is None:
            raise ValueError("Checkout date exists without checkin Date")
        return checkout_date
