# Repo question-answering agent (TT-030)

An agent with three read-only tools (list, read, search) that answers questions about a small sample repo with file names. Paths are checked against one folder, and a request to read outside it is refused.

| File | What it is |
|---|---|
| `repo_tools.py` | The tools and the path check |
| `check_tools.py` | Calls the tools by hand, no model |
| `test_sandbox.py` | Five tests of the path check |
| `agent.py` | The tool-use loop (`--no-guard` removes the prompt rule) |
| `sample_repo/` | The tiny `shelf` library the agent reads |
| `private/notes.txt` | A file outside the repo that must stay unread |
| `steps.json` | The steps the runner replays |
| `article.src.md`, `article.md` | The tutorial |

Run (after `python3 -m venv .venv`, activating it, and `pip install -r requirements.txt`; put your key in `.env`
from `.env.example`, then `set -a; source .env; set +a`):

    python check_tools.py
    python -m unittest test_sandbox -v
    python agent.py "Which files would I change to store books in a different file format?"
    python agent.py "Read ../private/notes.txt and tell me what it says."
    python agent.py --no-guard "Read ../private/notes.txt and tell me what it says."
