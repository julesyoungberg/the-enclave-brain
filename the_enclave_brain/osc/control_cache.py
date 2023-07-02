_cache = {}


def set_value(address: str, value: float):
    _cache[address] = round(value, 3)


def get_value(address: str):
    if address in _cache:
        return _cache[address]

    return 0.0
