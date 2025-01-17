import json
import requests  # type: ignore
from requests import Response  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from requests.packages.urllib3.util.retry import Retry  # type: ignore
from typing import NoReturn

from dopc.tools.venueAuth import venueAuth
from dopc.tools.constant import VenueBaseUrl
from logging import Logger
from dopc.tools.logs import getConsoleLoger


DEFAULT_TIMEOUT: int = 5  # seconds
venueLogger: Logger = getConsoleLoger('venue')

def handle_failed_response(response: Response, url: str) -> NoReturn| dict:
    if response.status_code in [404]:
        venueLogger.error(response.text)
        venueLogger.error(f'failed getting venue info from {url}')
        return {'msge': f'failed getting venue info from {url}'}
    else:
        venueLogger.error(f'failed getting venue info from {url}')
        raise Exception('failed getting venue info from {url}')


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class Venue:
    def __init__(self, venue_slug: str) -> None:
        self.dynamic_url = VenueBaseUrl.DYNAMIC_URL.format(VENUE_SLUG=venue_slug)
        self.static_url = VenueBaseUrl.DYNAMIC_URL.format(VENUE_SLUG=venue_slug)
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
        if venueAuth().auth_required:
            auth_header = venueAuth.get_token()
            s.headers.update(auth_header)
        self.session = s

    def getDynamicIfo(self) -> list[dict]:
        dynamic_url = self.dynamic_url
        response = self.session.request("GET", url=dynamic_url)
        #response = requests.request("GET", dynamic_url)
        if response.status_code == 200:
            values = json.loads(response.text).get("venue")
        else:
            values = handle_failed_response(response, dynamic_url)
        return values

    def getStaticicIfo(self) ->  list[dict]:
        dynamic_url = self.static_url
        response = self.session.request("GET", url=static_url)
        #response = requests.request("GET", dynamic_url)
        if response.status_code == 200:
            values = json.loads(response.text).get("venue")
        else:
            handle_failed_response(response, static_url)
        return values

    def parseDynamicInfo(self, input):
        pass

