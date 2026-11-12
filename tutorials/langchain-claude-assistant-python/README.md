# Personal assistant with LangChain and Claude (RB-035)

A small command-line assistant built with LangChain's `create_agent`, `claude-haiku-5-5`, a prompt template, in-memory conversation memory (LangGraph checkpointer) and two local tools: a calculator and a notes-file reader.

| File | What it does |
| --- | --- |
| `assistant.py` | The assistant: prompt template, agent, memory, chat loop (calls the Anthropic API) |
| `tools.py` | The `calculator` and `read_notes` tools; run it alone to test them without a model |
| `notes.txt` | Made-up notes the assistant can read |
| `steps.json` | The steps the evidence runner replays |
| `article.src.md`, `article.md` | The tutorial source and the built article |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python tools.py
cp .env.example .env   # then put your key in .env
set -a; source .env; set +a
python assistant.py "My name is Sam." "What do my notes say about the budget?" "What is my name?"
```

`assistant.py` needs `ANTHROPIC_API_KEY`. Memory lives in the running process only, so a new run starts empty.
