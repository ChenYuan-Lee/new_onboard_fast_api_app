from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, validator, conlist, conint


class DatesAndPriceCheckInputValidator(BaseModel):
    listing_ids: conlist(conint(gt=0), min_items=1)
    desired_checkin:Optional[date]

    @validator('desired_checkin')
    def date_must_be_greater_than_today(cls, date:Optional[date]) -> Optional[date]:
        if date < datetime.today().date():
            raise ValueError('Date must be after today' + str(date) + " " + str(datetime.today()))
        return date


