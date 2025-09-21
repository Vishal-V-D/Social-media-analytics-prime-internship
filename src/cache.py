
import time

_cache = {}
TTL = 60  

def get_from_cache(key):
    if key in _cache:
        value, expiry = _cache[key]
        if time.time() < expiry:
            return value
        else:
            del _cache[key] 
    return None

def set_cache(key, value):
    _cache[key] = (value, time.time() + TTL)
