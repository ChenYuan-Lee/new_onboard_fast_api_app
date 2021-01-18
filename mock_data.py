from datetime import date

from models.available_range_model import AvailableRange
from models.house_model import House

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
    ),
    2: House(
        listing_id=2,
        available_ranges=[
            AvailableRange(
                range_start=date(2021, 7, 1),
                range_end=date(2021, 7, 5)
            ),
            AvailableRange(
                range_start=date(2021, 11, 31),
                range_end=date(2022, 1, 5)
            ),
        ],
        min_stay_nights=5
    ),
    3: House(
        listing_id=3,
        available_ranges=[
            AvailableRange(
                range_start=date(2021, 5, 1),
                range_end=date(2021, 6, 5)
            ),
            AvailableRange(
                range_start=date(2021, 7, 31),
                range_end=date(2022, 1, 5)
            ),
        ],
        min_stay_nights=3
    )
}
