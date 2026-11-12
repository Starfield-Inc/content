"""Read public model metadata and raw files from Hugging Face. No token."""
import time

import requests

HEADERS = {"User-Agent": "starfield-labs-tutorial/1.0"}
PAUSE = 1.0  # seconds between calls
MAX_CHARS = 200_000


class NotFound(Exception):
    pass


def _get(url):
    response = requests.get(url, headers=HEADERS, timeout=30)
    time.sleep(PAUSE)
    if response.status_code in (401, 404):  # the Hub answers 401 for a name that does not exist
        raise NotFound(url)
    if response.status_code == 429:
        raise SystemExit("Rate limited by Hugging Face. Wait a few minutes and try again.")
    response.raise_for_status()
    return response


def model_info(model_id):
    """The model's public record: tags, card data and the list of files."""
    return _get(f"https://huggingface.co/api/models/{model_id}").json()


def raw_file(model_id, filename):
    """Text of one file on the main branch (the Hub redirects to its cache; requests follows)."""
    return _get(f"https://huggingface.co/{model_id}/raw/main/{filename}").text[:MAX_CHARS]
