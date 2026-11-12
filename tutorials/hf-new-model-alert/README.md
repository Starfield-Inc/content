# Get an alert when a new model appears on Hugging Face

Lists new models from chosen organisations using Hugging Face's public models API, drops copies and variants of other people's models, remembers what it has already reported, and writes a message to the terminal and to a text file. No account and no API key.

| File | What it does |
| --- | --- |
| `orgs.txt` | The organisations to watch, one per line (case sensitive) |
| `hfapi.py` | Calls the API with a User-Agent, a small limit and a pause |
| `filters.py` | Date window and the rules that find copies and fine-tunes |
| `compare_filters.py` | Counts what each candidate rule drops, for seven organisations |
| `show_one.py` | Prints the fields the API gives for one model |
| `hf_alert.py` | The alert: fetch, filter, remember, message |
| `forget.py` | Pretends the newest model is new again |
| `tests/test_filters.py` | Checks the rules on fixed records |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python compare_filters.py
python hf_alert.py
```

State is kept in `seen.json`, messages in `alerts.txt`. Both are ignored by git. Output depends on live data and on the date.
