from dataclasses import dataclass
from typing import List

from models.available_range_model import AvailableRange


@dataclass
class House:
    listing_id: int
    available_ranges: List[AvailableRange]
    min_stay_nights: int
