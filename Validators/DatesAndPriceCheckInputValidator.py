from pydantic.types import conint, conlist

from Validators.CheckinCheckoutValidator import CheckinCheckoutValidator


class DatesAndPriceCheckInputValidator(CheckinCheckoutValidator):
    listing_ids: conlist(conint(gt=0), min_items=1)
