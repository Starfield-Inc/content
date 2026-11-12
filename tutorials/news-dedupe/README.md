# News without the repeats

Reads public RSS feeds, groups headlines that are about the same story, and shows the groups on a local web page.

| File | What it does |
| --- | --- |
| `feeds.txt` | One feed address per line |
| `fetch_feeds.py` | Reads the feeds and saves titles and links to `items.json` |
| `dedupe.py` | Groups similar headlines from different feeds |
| `tests/test_dedupe.py` | Checks the grouping rule on fixed headlines |
| `app.py` | Shows the groups at http://127.0.0.1:8011/ |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python fetch_feeds.py
python dedupe.py
python -m unittest discover -s tests -v
python app.py
```

Only titles and links are saved. Each link goes to the publisher's page.
