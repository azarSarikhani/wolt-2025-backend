import os


token = os.environ.get('token') or 'dummy'


class venueAuth:
    def __init__(self) -> None:
        self.auth_required = False

    def get_token() -> dict[str, str]:
        headers = {
            'Authorization': f'Bearer {token}'
        }
        return headers
