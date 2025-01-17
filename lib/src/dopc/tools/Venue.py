import json
import requests  # type: ignore
from requests import Response  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from requests.packages.urllib3.util.retry import Retry  # type: ignore
from typing import NoReturn

from dopc.tools.venueAuth import venueAuth
from dopc.tools.constant import VenueBaseUrl, VenueDynamicPath, VenueStaticPath
from logging import Logger
from dopc.tools.logs import getConsoleLoger


DEFAULT_TIMEOUT: int = 5  # seconds
venueLogger: Logger = getConsoleLoger('venue')


def handle_failed_response(response: Response, url: str) -> NoReturn | dict:
    if response.status_code in [404]:
        venueLogger.error(response.text)
        venueLogger.error(f'failed getting venue info from {url}')
        return {'msge': f'failed getting venue info from {url}'}
    else:
        venueLogger.error(f'failed getting venue info from {url}')
        raise Exception('failed getting venue info from {url}')


def get_nested_dict(_input: dict, keys: [list]):
    try:
        for key in keys:
            _input = _input.get(key)
    except AttributeError:
         _input = None
    return _input


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
        response = self.session.request("GET", url=dynamic_url, verify=False)
        if response.status_code == 200:
            values = json.loads(response.text)
        else:
            values = handle_failed_response(response, dynamic_url)
        return values

    def getStaticicIfo(self) -> list[dict]:
        static_url = self.static_url
        response = self.session.request("GET", url=static_url, verify=False)
        if response.status_code == 200:
            values = json.loads(response.text)
        else:
            handle_failed_response(response, static_url)
        return values

    def parseVenueDynamicInfo(self, response_dict: dict):
        parsed_info: dict = {}
        items_to_collect = [
             VenueDynamicPath.ORDER_MINIMUM_NO_SURCHARGE,
             VenueDynamicPath.BASE_PRICE,
             VenueDynamicPath.DISTANCE_RANGES
        ]
        #order_minimum_no_surcharge_name = VenueDynamicPath.ORDER_MINIMUM_NO_SURCHARGE.name
        #order_minimum_no_surcharge_keys = VenueDynamicPath.ORDER_MINIMUM_NO_SURCHARGE.value
        #base_price_keys = VenueDynamicPath.BASE_PRICE.value
        #distance_ranges_keys = VenueDynamicPath.DISTANCE_RANGES.value
        for item in items_to_collect:
            #return parsed_info[item.name: 2]
            value = get_nested_dict(response_dict, item.value)
            if value:
                parsed_info.update({item.name: value})

        #min_order = get_nested_dict(response_dict, order_minimum_no_surcharge_keys)
        #base_price = get_nested_dict(response_dict, base_price_keys)
        #distance_ranges = get_nested_dict(response_dict, distance_ranges_keys)

        #parsed_info = {
        #    "order_minimum_no_surcharge": min_order,
        #    "base_price": base_price,
        #    "distance_ranges": distance_ranges
        #}
        return parsed_info
