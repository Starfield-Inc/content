"""Call Hugging Face's public models API politely."""
import re
import time

import requests

API = "https://huggingface.co/api/models"
HEADERS = {"User-Agent": "starfield-labs-tutorial/1.0"}
FIELDS = ["createdAt", "tags", "gated", "downloads"]
PAUSE = 1.0  # seconds between calls


class RateLimited(Exception):
    pass


def calls_left(response):
    """The API sends a header like: "api";r=499;t=222 (r = calls left, t = seconds to reset)."""
    match = re.search(r"r=(\d+)", response.headers.get("ratelimit", ""))
    return int(match.group(1)) if match else None


def newest_models(org, limit=30, session=None):
    """Return (models, calls_left) for the newest models of one organisation."""
    session = session or requests
    params = {"author": org, "sort": "createdAt", "direction": -1, "limit": limit, "expand[]": FIELDS}
    response = session.get(API, params=params, headers=HEADERS, timeout=30)
    if response.status_code == 429:
        raise RateLimited(f"Rate limited. Try again in about {response.headers.get('retry-after', 'a few')} seconds.")
    response.raise_for_status()
    time.sleep(PAUSE)
    return response.json(), calls_left(response)
