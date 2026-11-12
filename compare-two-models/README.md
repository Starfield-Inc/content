# Compare two models side by side

A page that sends one prompt to two Claude models and shows two columns with the answer, time taken, tokens used and a cost worked out from the listed prices. Tutorial TT-007.

| File | What it does |
| --- | --- |
| `models.py` | The two model IDs, their prices and the thinking setting each one needs |
| `compare.py` | Sends one prompt to both models; command line use and the shared function |
| `app.py` | FastAPI app: `POST /compare` and the page at `/` |
| `index.html` | The two-column page |
| `test_cost.py` | Checks the cost arithmetic with fixed numbers (no API call) |
| `test_route.py` | Calls the running route once |
| `spend_log.py` | Budget helper: one line per call in `spend.log` |
| `steps.json` | The steps the runner replays |

Run (after `python3 -m venv .venv` and activating it):

```bash
pip install -r requirements.txt
cp .env.example .env   # then put your key in .env and load it
python compare.py "Explain what an API rate limit is, in two sentences, for a beginner." --save demo_result.json
uvicorn app:app --port 8042
```

Open `http://127.0.0.1:8042/` or `http://127.0.0.1:8042/?demo=1` (saved result, no calls).
