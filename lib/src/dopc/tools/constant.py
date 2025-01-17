from enum import Enum
from strenum import StrEnum


class VenueBaseUrl(StrEnum):
    STATIC_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{VENUE_SLUG}/static"
    DYNAMIC_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{VENUE_SLUG}/dynamic"


class VenueDynamicPath(Enum):
    MINIMUM_NO_SURCHARGE = ["venue_raw","delivery_specs","rder_minimum_no_surcharge"]

