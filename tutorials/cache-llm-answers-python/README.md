# Cache LLM answers (TT-034)

A small cache in front of the Anthropic API. It hashes the request, returns a stored answer on a hit, drops entries after an expiry time, and counts the calls and tokens it saved on a test set.

| File | What it is |
|---|---|
| `llm_cache.py` | `make_key`, the `Cache` class (JSON file, expiry) and `ask` |
| `ask_many.py` | Runs `questions.txt` through the cache and prints hits, misses, tokens and timings |
| `key_demo.py` | Shows which changes give a new cache key (no API call) |
| `expiry_demo.py` | Shows an entry expiring after a 2 second lifetime |
| `temperature_probe.py` | Sends a temperature once and shows the API refuses it for this model |
| `test_cache.py` | Fixed-data check that empty replies are not cached (no API call) |
| `questions.txt` | The test set: 7 lines, 2 exact repeats and 1 messy repeat |
| `steps.json` | The steps the runner replays |
| `article.src.md`, `article.md` | The tutorial |

Run (after `python3 -m venv .venv`, activating it, and `pip install -r requirements.txt`; put your key in `.env`
from `.env.example`, then `set -a; source .env; set +a`):

    python key_demo.py
    python ask_many.py questions.txt
    python ask_many.py questions.txt
    python ask_many.py questions.txt --normalize --cache cache-normalized.json
    python temperature_probe.py
    python expiry_demo.py
    python test_cache.py

Delete `cache*.json` to start from an empty cache.
