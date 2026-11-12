# Chroma knowledge base chatbot (RB-031)

Stores nine short notes about a made-up hackathon team in a local Chroma vector store, retrieves the closest chunks for a question, and has `claude-haiku-5-5` answer from those chunks only, with file-name citations and "not in the notes" when the answer is absent.

| File | What it does |
| --- | --- |
| `notes/*.md` | Nine short notes about a fictional team (written for this tutorial) |
| `kb.py` | Chunker and the Chroma client |
| `warm_up.py` | Loads Chroma's default embedding model (downloads it once, about 79 MB) |
| `ingest.py` | Reads the notes, chunks them, stores them in `chroma_db/` |
| `search.py` | Prints the closest chunks for a question (no key needed) |
| `ask.py` | Retrieves chunks and asks the model to answer from them (needs `ANTHROPIC_API_KEY`) |
| `steps.json` | The steps the evidence runner replays |
| `article.src.md`, `article.md` | The tutorial source and the built article |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python warm_up.py
python ingest.py
python search.py "Who is cleaning the tide data?"
cp .env.example .env   # then put your key in .env
set -a; source .env; set +a
python ask.py "Why did the team choose SQLite?"
python ask.py "How much did the team spend on food during the event?"
```
