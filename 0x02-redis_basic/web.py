#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import redis
import time
from functools import wraps

# Redis connection
redis_client = redis.Redis()

def cache_result(expiration):
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            cache_key = f"count:{url}"
            result = redis_client.get(cache_key)
            if result is not None:
                return result.decode("utf-8")

            content = func(url)
            redis_client.setex(cache_key, expiration, content)
            return content

        return wrapper

    return decorator

@cache_result(expiration=10)
def get_page(url):
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://example.com"
    content = get_page(url)
    print(content)

