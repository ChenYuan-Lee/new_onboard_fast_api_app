from dataclasses import dataclass
from datetime import date


@dataclass
class AvailableRange:
    range_start: date
    range_end: date
