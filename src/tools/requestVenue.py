import requests  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from requests.packages.urllib3.util.retry import Retry  # type: ignore
from venueAuth import venueAuth


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
            auth_header = get_token()
            s.headers.update(auth_header)
        self.session = s

