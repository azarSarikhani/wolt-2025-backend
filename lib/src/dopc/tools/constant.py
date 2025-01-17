from enum import Enum
from strenum import StrEnum


class VenueBaseUrl(StrEnum):
    STATIC_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{VENUE_SLUG}/static"
    DYNAMIC_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{VENUE_SLUG}/dynamic"


class VenueDynamicPath(Enum):
    ORDER_MINIMUM_NO_SURCHARGE = ["venue_raw", "delivery_specs", "order_minimum_no_surcharge"]
    BASE_PRICE = ["venue_raw" , "delivery_specs" , "delivery_pricing" , "base_price"]
    DISTANCE_RANGES = ["venue_raw" , "delivery_specs" , "delivery_pricing" , "distance_ranges"]


class VenueStaticPath(Enum):
    COORDINATES = ["venue_raw" , "location" , "coordinates"]
