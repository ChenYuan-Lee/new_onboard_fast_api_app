from datetime import datetime

from pydantic import BaseModel, validator


class DatesAndPriceCheckInputValidator(BaseModel):
    listing_ids: list
    desired_checkin: str

    @validator('listing_ids')
    def listing_must_greater_than_zero(cls, v):
        if len(v) < 0:
            raise ValueError("Too few listings to check on")
        return v

    @validator('desired_checkin')
    def date_must_be_greater_than_today(cls, d):
        date_time_obj = datetime.strptime(d, '%Y-%m-%d')
        if date_time_obj < datetime.now():
            raise ValueError('Date must be after today' + d + " " + str(datetime.today()))
        return d


