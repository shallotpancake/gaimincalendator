import os
import time

CACHE_FILE = 'cache.html'
CACHE_TIMESTAMP_FILE = 'cache_timestamp.txt'
CACHE_DURATION = 3600  # Cache duration in seconds (1 hour)

def cache_response(response_text):
    with open(CACHE_FILE, 'w', encoding='utf-8') as file:
        file.write(response_text)
    with open(CACHE_TIMESTAMP_FILE, 'w', encoding='utf-8') as file:
        file.write(str(time.time()))

def is_cache_valid():
    if not os.path.exists(CACHE_TIMESTAMP_FILE):
        return False
    with open(CACHE_TIMESTAMP_FILE, 'r', encoding='utf-8') as file:
        timestamp = float(file.read())
    return (time.time() - timestamp) < CACHE_DURATION
