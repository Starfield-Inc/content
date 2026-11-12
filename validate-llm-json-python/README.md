# Validate LLM JSON output with a schema (TT-032)

A small Python function that asks Claude for JSON, checks it against a pydantic schema, retries once with the error message, and counts failures over 50 runs for a loose prompt and a strict prompt.

| File | What it is |
|---|---|
| `schema.py` | The pydantic `Ticket` model: allowed categories, priority 1 to 5, summary length |
| `ask_json.py` | `ask_json()`: call, validate, retry once with the error text. Strict and loose prompts |
| `check_fixed.py` | No API call. Fixed strings the schema accepts or rejects |
| `ask_one.py` | Four support messages through the strict prompt, no retry |
| `fail_demo.py` | A real failure with the loose prompt, then the retry |
| `count_failures.py` | 50 runs with `loose` or `strict`, counts failures and retries |
| `steps.json` | The steps the runner replays |
| `article.src.md`, `article.md` | The tutorial |

Run (after `python3 -m venv .venv`, activating it, and `pip install -r requirements.txt`; put your key in `.env`
from `.env.example`, then `set -a; source .env; set +a`):

    python check_fixed.py
    python ask_one.py
    python fail_demo.py
    python count_failures.py loose
    python count_failures.py strict

Replies differ between runs, so counts will not match the article exactly.
