# Stream an answer to a web page (TT-003)

A FastAPI server that streams a model answer to a page as server-sent events, with a saved-answer route for rehearsal and a way to resume a dropped connection.

| File | What it is |
|---|---|
| `prompt.py` | Model name, token cap and the fixed prompt |
| `timing.py` | One streamed API call, prints opening-chunk and total time, saves `cache.json` |
| `app.py` | FastAPI app: `GET /demo` (saved or `?live=1`), `GET /health`, page at `/` |
| `index.html` | The page (plain JavaScript, `EventSource`) |
| `test_drop.py` | Drops a connection after 4 events and resumes it (no API call) |
| `leave_early.py` | Opens a live stream and leaves after 3 events |
| `spend_log.py` | Budget helper: one line per API call in `spend.log` |
| `steps.json` | The steps the runner replays |
| `article.src.md`, `article.md` | The tutorial |

Run (venv active, packages installed, key exported from `.env`):

    python timing.py
    uvicorn app:app --port 8041        # terminal 1
    python test_drop.py                # terminal 2
    # open http://127.0.0.1:8041/
