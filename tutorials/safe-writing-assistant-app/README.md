# Draft helper with a safety layer (RB-025)

A small Flask app. You paste a draft and get three suggestions from Claude. Before any suggestion is made, the server checks the length, asks a second Claude call to screen the draft, and keeps the API key on the server.

| File | What it does |
| --- | --- |
| `safety.py` | Length limit (1500 characters), checked before any model call |
| `assistant.py` | The moderation call, the suggestion call and both system prompts |
| `app.py` | Flask server: the page and `POST /api/suggest` |
| `templates/index.html` | The page, with a character counter |
| `drafts.py` | Fixed example drafts written for this tutorial |
| `test_safety.py` | Unit tests for the length check (no key needed) |
| `demo_moderation.py`, `try_endpoint.py`, `check_leak.py` | Scripts that show each safety check working |
| `steps.json` | The steps the evidence runner replays |
| `article.src.md`, `article.md` | The tutorial source and the built article |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m unittest -v test_safety
cp .env.example .env   # then put your key in .env
set -a; source .env; set +a
python demo_moderation.py
python app.py          # open http://127.0.0.1:8125/
python try_endpoint.py # in a second terminal, with the key loaded there too
```

The app and the demo scripts need `ANTHROPIC_API_KEY`. Model replies differ from run to run.
