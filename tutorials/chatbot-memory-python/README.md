# Chatbot with memory (TT-010)

Terminal chatbot that keeps the message list between turns, shows token counts and trims old messages.

| File | What it is |
|---|---|
| `forgetful.py` | Two calls with no memory |
| `chat.py` | The chatbot: message list, token counts, `--keep N` trimming |
| `script.txt` | Four scripted user lines, piped in so the run is repeatable |
| `spend_log.py` | Budget helper: one line per API call in `spend.log` |
| `steps.json` | The steps the runner replays |
| `article.src.md`, `article.md` | The tutorial |

Run (after `python3 -m venv .venv`, activating it, and `pip install -r requirements.txt`; put your key in `.env`
from `.env.example`, then `set -a; source .env; set +a`):

    python forgetful.py
    python chat.py < script.txt
    python chat.py --keep 4 < script.txt
