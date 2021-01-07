from datetime import date


class DatesCheck:

    def __init__(
            self,
            listing_id: int,
            next_available_checkin_date: date
    ):
        self.listing_id = listing_id
        self.next_available_checkin_date = next_available_checkin_date
