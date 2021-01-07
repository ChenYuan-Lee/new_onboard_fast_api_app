from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class AvailableRange:
    range_start: date
    range_end: date


@dataclass
class House:
    listing_id: int
    available_ranges: List[AvailableRange]
    min_stay_nights:int


data = {
    1: House(
        listing_id=1,
        available_ranges=[
            AvailableRange(
                range_start=date(2021, 8, 1),
                range_end=date(2021, 12, 5)
            ),
            AvailableRange(
                range_start=date(2021, 12, 31),
                range_end=date(2022, 2, 5)
            ),
        ],
        min_stay_nights=3
    )
}
