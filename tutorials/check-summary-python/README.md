# Check an AI summary against its source (TT-027)

Script that lists the claims in a summary, asks a model to quote the source sentence for each, checks the quote and numbers in code, and prints a found / not found report.

| File | What it is |
|---|---|
| `check_summary.py` | The checker: `python check_summary.py source.txt summary.txt` |
| `source.txt` | An invented source text written for this tutorial |
| `summary_good.txt` | A faithful summary |
| `summary_bad.txt` | A summary with four planted errors |
| `test_judge.py` | Fixed-data test of the code-side checks, no API call |
| `spend_log.py` | Budget helper: one line per API call in `spend.log` |
| `steps.json` | The steps the runner replays |
| `article.src.md`, `article.md` | The tutorial |

Run (after `python3 -m venv .venv`, activating it, and `pip install -r requirements.txt`; put your key in `.env`
from `.env.example`, then `set -a; source .env; set +a`):

    python check_summary.py source.txt summary_good.txt
    python check_summary.py source.txt summary_bad.txt
    python test_judge.py
