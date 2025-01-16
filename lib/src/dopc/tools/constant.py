from strenum import StrEnum


class VenueBaseUrl(StrEnum):
    STATIC_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{VENUE_SLUG}/static"
    DYNAMIC_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{VENUE_SLUG}/dynamic"
