from datetime import date


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
