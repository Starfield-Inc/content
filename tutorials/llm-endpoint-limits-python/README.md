# Rate limit and spending cap for an LLM endpoint (TT-036)

A FastAPI endpoint that limits requests per user, stops at a daily cost cap computed from real API usage, and logs blocked calls.

| File | What it is |
|---|---|
| `limits.py` | `RateLimiter` (sliding window per user), `DailyCap`, `cost_usd`, and the example price constants |
| `app.py` | The FastAPI app: `POST /ask`, `GET /usage` |
| `test_limits.py` | Checks for the two guards with fixed numbers and a fake clock (no API call) |
| `demo.py` | Starts the real server on port 8136 and sends real requests: `rate`, `cap`, `restart`, `logs` |
| `steps.json` | The steps the runner replays |
| `article.src.md`, `article.md` | The tutorial |

Run (after `python3 -m venv .venv`, activating it, and `pip install -r requirements.txt`; put your key in `.env`
from `.env.example`, then `set -a; source .env; set +a`):

    python test_limits.py
    python demo.py rate
    python demo.py cap
    python demo.py logs
    python -m uvicorn app:app --port 8136

The prices in `limits.py` are example values. Check the current price list before you rely on the cost numbers.
