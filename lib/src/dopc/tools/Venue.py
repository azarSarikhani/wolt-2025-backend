import requests  # type: ignore
from requests import Response  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from requests.packages.urllib3.util.retry import Retry  # type: ignore
from typing import NoReturn

from dopc.tools.venueAuth import venueAuth
from dopc.tools.constant import VenueBaseUrl
from logging import Logger


def handle_failed_response(response: Response, url: str, venue_slug: str, logger: Logger) -> NoReturn:
    if response.status_code in [401, 403]:
        logger.error(response.text)
        logger.error(f'failed getting {venue_slug} from {url}')
        raise Exception('failed getting {venue_slug} from {url}')
    else:
        logger.error(f'failed getting {venue_slug} from {url}')
        raise Exception('failed getting {venue_slug} from {url}')


class Venue:
    def __init__(self, url: str) -> None:
        self.url = url
        self.config = read_config(config_filename)
        s = requests.Session()
        retry_strategy = Retry(
            total=5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            backoff_factor=2
        )
        adapter = TimeoutHTTPAdapter(max_retries=retry_strategy)
        s.mount('https://', adapter)
        s.mount('http://', adapter)
        if venueAuth.auth_required:
            auth_header = venueAuth.get_token()
            s.headers.update(auth_header)
        self.session = s
    def getDynamicIfo(self, venue_slug: str, logger) ->  list[dict]:
        dynamic_url = VenueBaseUrl.DYNAMIC_URL.format(VENUE_SLUG=venue_slug)
        response = self.session.request("GET", url=dynamic_url)
        if response.status_code == 200:
            return response
            values = json.loads(response.text).get("venue")
        else:
            handle_failed_response(response, dynamic_url, venue_slug, logger)
        return values
    def getDynamicIfo(self, venue_slug: str, logger) ->  list[dict]:
        static_url = VenueBaseUrl.DYNAMIC_URL.format(VENUE_SLUG=venue_slug)
        response = self.session.request("GET", url=static_url)
        if response.status_code == 200:
            return response
            values = json.loads(response.text).get("venue")
        else:
            handle_failed_response(response, static_url, venue_slug, logger)
        return values

