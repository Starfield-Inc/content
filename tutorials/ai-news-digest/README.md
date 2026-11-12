# AI news digest from RSS feeds (TT-019)

Reads five public AI news feeds, removes duplicates, writes a one-sentence summary of each item with an LLM, and builds a page with the source link beside every summary.

| File | What it is |
|---|---|
| `feeds.txt` | The five feed addresses |
| `fetch_feeds.py` | Reads the feeds with feedparser into a JSON file |
| `dedupe.py` | Drops items with the same link or title |
| `summarise.py` | One model call per item; the link is copied from the feed, never from the model |
| `build_page.py` | Writes `digest.html` and `digest.md` |
| `spend_log.py` | Budget helper: one line per API call in `spend.log` |
| `sample_items.json` | Invented example items used for the published screenshots (no third-party headlines) |
| `steps.json` | The steps the runner replays |
| `article.src.md`, `article.md` | The tutorial |

Run (after `python3 -m venv .venv`, activating it, and `pip install -r requirements.txt`; put your key in `.env`
from `.env.example`, then `set -a; source .env; set +a`):

    python fetch_feeds.py --out live/items.json
    python dedupe.py sample_items.json unique.json
    python summarise.py unique.json summaries.json --limit 5
    python build_page.py summaries.json
    python -m http.server 8019 --bind 127.0.0.1   # then open /digest.html

Live feeds change every day, so a live run gives different items from the saved evidence.
