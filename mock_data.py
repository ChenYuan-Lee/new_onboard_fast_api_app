from typing import List


class ListingsDataDB:
    LISTINGS_DATA = {
        1: {
            "listing_id": 1,
            "bedrooms": 2,
            "bathrooms": 2.5,
        },
        2: {
            "listing_id": 2,
            "bedrooms": 3,
            "bathrooms": 1.5,
        },
        3: {
            "listing_id": 3,
            "bedrooms": 4,
            "bathrooms": 2,
        },
    }

    @classmethod
    def get_listings_data_from_db(cls, listing_ids: List[int]) -> List[dict]:
        print(f"Call made to {cls.__name__} for listing ids {listing_ids}.")
        return [cls.LISTINGS_DATA[listing_id] for listing_id in listing_ids]


class PricesDataDB:
    PRICES_DATA = {
        1: 441.43,
        2: 242.63,
        3: 141.43,
    }

    @classmethod
    def get_prices_data_from_db(cls, listing_ids: List[int]) -> List[float]:
        print(f"Call made to {cls.__name__} for listing ids {listing_ids}.")
        return [cls.PRICES_DATA[listing_id] for listing_id in listing_ids]
