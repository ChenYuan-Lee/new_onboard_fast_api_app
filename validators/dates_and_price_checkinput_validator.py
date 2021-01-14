from pydantic.types import conint, conlist

from validators.checkin_checkout_validator import CheckinCheckoutValidator


class DatesAndPriceCheckInputValidator(CheckinCheckoutValidator):
    listing_ids: conlist(conint(gt=0), min_items=1)
