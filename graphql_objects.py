from datetime import date

from typing import Union


class DatesCheck:

    def __init__(
            self,
            listing_id: int,
            is_available: bool,
            checkin_date: date,
            checkout_date: date,
    ):
        self.listing_id = listing_id
        self.is_available = is_available
        self.checkin_date = checkin_date
        self.checkout_date = checkout_date


class Error:
    def __init__(
            self,
            error: str,
    ):
        self.error = error


class ListingUnsupportedError(Error):
    def __init__(
            self,
            error: str,
    ):
        super().__init__(error)
        self.error = error


class GenericError(Error):
    def __init__(
            self,
            error: str
    ):
        super().__init__(error)
        self.error = error


DateResults = Union[DatesCheck, ListingUnsupportedError, GenericError]
