import sys


def __call__(inputs: dict) -> dict[str, float]:
    # toeo
    return {'price': 10}


# Rejected: https://peps.python.org/pep-0713/
sys.modules[__name__] = __call__
