from datetime import date

from Models.AvailableRangeModel import AvailableRange
from Models.HouseModel import House

data = {
    1: House(
        listing_id=1,
        available_ranges=[
            AvailableRange(
                range_start=date(2021, 8, 1),
                range_end=date(2021, 8, 5)
            ),
            AvailableRange(
                range_start=date(2021, 12, 31),
                range_end=date(2022, 2, 5)
            ),
        ],
        min_stay_nights=3
    )
}
