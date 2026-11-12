# Hackathon demo chatbot (TT-002)

A FastAPI backend and one HTML page for a small demo chatbot.

| File | What it is |
|---|---|
| `one_call.py` | One API call, prints the reply and token counts |
| `app.py` | FastAPI app: `POST /chat`, `GET /health`, serves the page at `/` |
| `index.html` | The chat page (plain HTML and JavaScript) |
| `test_questions.py` | Sends five questions to the running server |
| `spend_log.py` | Budget helper: one line per API call in `spend.log` |
| `steps.json` | The steps the runner replays |
| `article.src.md`, `article.md` | The tutorial |

Run (venv active, packages installed, key exported from `.env`):

    python one_call.py
    uvicorn app:app --port 8031        # terminal 1
    python test_questions.py           # terminal 2
    # open http://127.0.0.1:8031/
